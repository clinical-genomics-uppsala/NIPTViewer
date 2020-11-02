from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
import random
import datetime

from dataprocessor.models import Flowcell, SamplesRunData, BatchRun, SampleType
from dataprocessor.utils.data import import_data_into_database
# Create your views here.

from .forms import UploadFileForm

from reportvisualiser.utils.plots import data_structur_generator
from reportvisualiser.utils.data import extract_data, decimal_default
from .utils import plots, colors, data

def index(request):
    """
            Information page showing flowcells that have been run and plot
            showing fetal fraction over time and NCV over time for controls
    """
    sample_run_data = SamplesRunData.objects.select_related().all().order_by('-flowcell_id__run_date')
    flowcell_run_data = BatchRun.objects.select_related().all().order_by('-flowcell_id__run_date')

    control_type = SampleType.objects.get(name="Control")
    control_flowcell_data = SamplesRunData.objects.select_related().filter(sample_type=control_type).order_by('-flowcell_id__run_date')
    context = {'flowcell_data': flowcell_run_data}

    if sample_run_data.exists():
        context['data_coverage'] = [plots.chromosome_coverage(data=sample_run_data)]
        context['data_ff_time'] = plots.fetal_fraction(data=sample_run_data)

    if control_flowcell_data.exists():
        context['ncd'] = plots.ncd_data(control_flowcell_data)

    template = loader.get_template("reportvisualiser/index.html")
    return HttpResponse(template.render(context, request))

def sample_report(request, barcode, sample):
    flowcell = Flowcell.get_flowcell(flowcell_barcode=barcode)
    flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell)
    previous_samples = SamplesRunData.objects.all().exclude(flowcell_id=flowcell)

    data = {
             'today': datetime.date.today().strftime("%Y-%m-%d"),
             'sample': flowcell_run_data,
             'flowcell_barcode': barcode,
             'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
             'page_type': "html"}

    data.update(data_structur_generator(samples_info))
    template = loader.get_template("reportvisualiser/sample_report.html")
    return HttpResponse(template.render(data, request))


def report(request, barcode):
    flowcell = Flowcell.get_flowcell(flowcell_barcode=barcode)
    samples_run_data = SamplesRunData.get_samples(flowcell=flowcell)
    flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell)

    sample_info = data.extract_info_samples(flowcell_other, data.sample_info.copy() , size=0.5, label=lambda x: 'other', color=colors.hist)
    color_dict, sample_info = data.extra_info_per_sample(samples_run_data, sample_info, label=lambda x: x.sample_id, size=1.0, shape="circle",colors=colors.samples)
    context = {'samples': [d.sample_id for d in samples_run_data], 'flowcell_barcode': barcode, 'flowcell_run_data': samples_run_data, 'color_dict': color_dict}
    context.update(data_structur_generator(sample_info))

    if samples_run_data.exists():
        context['data_coverage'] = plots.chromosome_coverage(data=samples_run_data)
        context['data_ff_time'] = plots.fetal_fraction(data=flowcell_other) + plots.fetal_fraction(data=samples_run_data, label=lambda x: barcode)

    template = loader.get_template("reportvisualiser/report.html")
    return HttpResponse(template.render(context, request))


def upload(request):
    import io
    context = {}
    template = loader.get_template("reportvisualiser/file_upload.html")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            flowcell = import_data_into_database(request.FILES['file'])
            if isinstance(flowcell, Flowcell):
                context['form_data'] = form
                context['file_validation'] = (flowcell.flowcell_barcode,flowcell.created)
                return HttpResponse(template.render(context, request))
            else:
                return redirect('viewer:report', barcode=flowcell)
        else:
            context['form_data'] = form
    else:
        context['form_data'] = UploadFileForm()
    return HttpResponse(template.render(context, request))
