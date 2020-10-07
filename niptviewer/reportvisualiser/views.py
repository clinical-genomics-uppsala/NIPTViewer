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
    context = {'flowcell_data': flowcell_data}

    batch_data = {'13': {'data': {}, 'fields': ('flowcell_id', 'median_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'median_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'median_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'median_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'median_y')}}
    batch_data = extract_data(flowcell_data, batch_data, lambda x: "median", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
    context['median_coverage'] = [{"key": k, 'values': d['data']['median']} for k,d in batch_data.items()]

    samples_info_ff_formated = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info_ff_formated = extract_data(SamplesRunData.objects.all(), samples_info_ff_formated, lambda x: 'hist',x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
    context = data_structur_generator(samples_info_ff_formated, context)

    template = loader.get_template("reportvisualiser/index.html")
    return HttpResponse(template.render(context, request))

def sample_report(request, barcode, sample):
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
    samples_info = extract_data(SamplesRunData.get_samples_not_included(flowcell=flowcell,sample=sample), samples_info, label=lambda x: 'other')

    samples_info = extract_data(flowcell_run_data, samples_info, label=lambda x: barcode)
    samples_info = extract_data(sample_flowcell_run_data, samples_info, label=lambda x: sample)
    data = {
             'today': datetime.date.today().strftime("%Y-%m-%d"),
             'sample': sample_flowcell_run_data,
             'flowcell_barcode': barcode,
             'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
             'page_type': "html"}
    data = data_structur_generator(samples_info, data)
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
    flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell)
    samples_info = extract_data(flowcell_other, samples_info, label=lambda x: 'other')
    samples_info = extract_data(flowcell_run_data, samples_info, label=lambda x: barcode)
    context = {'samples': [d.sample_id for d in flowcell_run_data], 'flowcell': barcode, 'flowcell_data': flowcell_run_data}
    context = data_structur_generator(samples_info, context)


    samples_info_ff_formated = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info_ff_formated = extract_data(flowcell_other, samples_info_ff_formated, lambda x: "hist",x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
    samples_info_ff_formated = extract_data(flowcell_run_data, samples_info_ff_formated, lambda x: barcode,x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
    context = data_structur_generator(samples_info_ff_formated, context)

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
