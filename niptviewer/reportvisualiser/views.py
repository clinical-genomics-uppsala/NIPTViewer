from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
import random

from dataprocessor.models import Flowcell, SamplesRunData, BatchRun
from dataprocessor.utils.data import import_data_into_database
# Create your views here.

from .forms import UploadFileForm

from reportvisualiser.utils.plots import extract_data, data_structur_generator, decimal_default


def index(request):
    flowcell_data = BatchRun.objects.select_related().all().order_by('-flowcell_id__run_date')
    batch_data = {'median_13': [], 'median_18': [], 'median_21': [], 'median_x': [],
            'median_y': [], 'stdev_13': [], 'stdev_18': [], 'stdev_21': [],
            'stdev_X': [], 'stdev_Y': []}
    for item in flowcell_data:
        for key in batch_data:
            batch_data[key].append({"y": decimal_default(getattr(item,key)), "x": item.flowcell_id.run_date.timestamp()*1000,'label': item.flowcell_id.flowcell_barcode})
    context = {'flowcell_data': flowcell_data}
    data = []
    for comparison in batch_data:
        if comparison.startswith("median"):
            data.append({'key': comparison, 'values': batch_data[comparison][::-1]})
    context['median_coverage'] = data
    template = loader.get_template("reportvisualiser/index.html")
    return HttpResponse(template.render(context, request))

def sample_report(request, barcode, sample):
    #from reportvisualiser.utils.pdf import render_to_pdf
    import datetime

    samples_info = {'x_vs_y': {'data': {}, 'fields': ('ncv_X', 'ncv_Y')},
               'x_vs_ff': {'data': {}, 'fields': ('ncv_X', 'ff_formatted')},
               'y_vs_ff': {'data': {}, 'fields': ('ncv_Y', 'ff_formatted')},
               'chr13_vs_ff': {'data': {}, 'fields': ('ncv_13', 'ff_formatted')},
               'chr18_vs_ff': {'data': {}, 'fields': ('ncv_18', 'ff_formatted')},
               'chr21_vs_ff': {'data': {}, 'fields': ('ncv_21', 'ff_formatted')}}

    flowcell = Flowcell.get_flowcell(flowcell_barcode=barcode)
    sample_flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell, sample_id=sample)
    flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell).exclude(sample_id=sample)
    samples_info = extract_data('other', SamplesRunData.get_samples_not_included(flowcell=flowcell,sample=sample), samples_info, only_prefix=True)

    samples_info = extract_data(barcode, flowcell_run_data, samples_info, only_prefix=True)
    samples_info = extract_data(sample, sample_flowcell_run_data, samples_info, only_prefix=True)

    data = {
             'today': datetime.date.today().strftime("%Y-%m-%d"),
             'sample': sample,
             'flowcell_barcode': barcode,
             'run_date': flowcell.run_date.strftime("%Y-%m-%d")}
    data = data_structur_generator(samples_info, data)
    #pdf = render_to_pdf('reportvisualiser/sample_report.html', data)
    #return HttpResponse(pdf, content_type='application/pdf')
    template = loader.get_template("reportvisualiser/sample_report.html")
    return HttpResponse(template.render(data, request))


def report(request, barcode):
    samples_info = {'x_vs_y': {'data': {}, 'fields': ('ncv_X', 'ncv_Y')},
               'x_vs_ff': {'data': {}, 'fields': ('ncv_X', 'ff_formatted')},
               'y_vs_ff': {'data': {}, 'fields': ('ncv_Y', 'ff_formatted')},
               'chr13_vs_ff': {'data': {}, 'fields': ('ncv_13', 'ff_formatted')},
               'chr18_vs_ff': {'data': {}, 'fields': ('ncv_18', 'ff_formatted')},
               'chr21_vs_ff': {'data': {}, 'fields': ('ncv_21', 'ff_formatted')}}

    flowcell = Flowcell.get_flowcell(flowcell_barcode=barcode)

    flowcell_run_data = SamplesRunData.get_samples(flowcell=flowcell)
    samples_info = extract_data('hist', SamplesRunData.get_samples_not_included(flowcell=flowcell), samples_info)
    samples_info = extract_data(barcode, flowcell_run_data, samples_info)

    context = data_structur_generator(samples_info, {'flowcell_data': flowcell_run_data})

    template = loader.get_template("reportvisualiser/report.html")
    return HttpResponse(template.render(context, request))


def upload(request):
    import io
    context = {}
    template = loader.get_template("reportvisualiser/file_upload.html")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            flowcell = import_data_into_database(request.FILES['file'])
            if isinstance(flowcell, Flowcell):
                context['form_data'] = form
                print("Instance...")
                context['file_validation'] = (flowcell.flowcell_barcode,flowcell.created)
                return HttpResponse(template.render(context, request))
            else:
                return redirect('viewer:report', barcode=flowcell)
        else:
            print("Invalid")
            context['form_data'] = form
    else:
        context['form_data'] = UploadFileForm()
    return HttpResponse(template.render(context, request))
