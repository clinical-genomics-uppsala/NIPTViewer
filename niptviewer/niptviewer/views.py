from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from dataprocessor.models import BatchRun, Flowcell, SamplesRunData, SampleType
from reportvisualiser.utils.plots import extract_data, data_structur_generator
from django.contrib import auth

from reportvisualiser.utils import plots

@login_required
def logout(request):
    auth.logout(request)
    return redirect("login")


def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(reverse("index"))
        else:
            context['login_error'] = "Invalid username or password"
            if request.POST['username']:
                context['username'] = request.POST['username']
    template = loader.get_template("base.html")
    return HttpResponse(template.render(context, request))

@login_required
def index(request):
    num_flowcells = Flowcell.objects.count()
    num_samples = SamplesRunData.objects.count()
    latest_flowcells = Flowcell.objects.all().order_by('-run_date')[:5]
    latest_samples = SamplesRunData.objects.all().order_by('-flowcell_id__run_date')[:5]
    control_flowcell_data = SamplesRunData.objects.select_related().filter(sample_type=SampleType.objects.get(name="Control")).order_by('-flowcell_id__run_date')
    sample_run_data = SamplesRunData.objects.all()

    context = {'num_flowcells': num_flowcells, 'num_samples': num_samples, 'latest_flowcells': latest_flowcells,'latest_samples': latest_samples}

    if sample_run_data.exists():
        context['data_ff_time'] = plots.fetal_fraction(data=sample_run_data)

    if control_flowcell_data.exists():
        context['ncd'] = plots.ncd_data(control_flowcell_data)

    template = loader.get_template("base.html")
    return HttpResponse(template.render(context, request))
