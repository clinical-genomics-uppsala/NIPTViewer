
from django.http import HttpResponse
from django.template import loader
from dataprocessor.models import Flowcell, SamplesRunData
from reportvisualiser.utils.plots import extract_data, data_structur_generator

def index(request):
    num_flowcells = Flowcell.objects.count()
    num_samples = SamplesRunData.objects.count()
    latest_flowcells = Flowcell.objects.all().order_by('-run_date')[:5]
    latest_samples = SamplesRunData.objects.all().order_by('-flowcell_id__run_date')[:5]
    samples_info = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info = extract_data('hist', SamplesRunData.objects.all(), samples_info, True,x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
    context = {'num_flowcells': num_flowcells,
    'num_samples': num_samples, 'latest_flowcells': latest_flowcells,'latest_samples': latest_samples}
    context = data_structur_generator(samples_info, context)
    template = loader.get_template("base.html")
    return HttpResponse(template.render(context, request))
