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
    coverage_data =[{
            'key': sample.sample_id, 'data': [
            {'x': 0, 'y': decimal_default(sample.chr1_coverage)},
            {'x': 1, 'y': decimal_default(sample.chr2_coverage)},
            {'x': 2, 'y': decimal_default(sample.chr3_coverage)},
            {'x': 3, 'y': decimal_default(sample.chr4_coverage)},
            {'x': 4, 'y': decimal_default(sample.chr5_coverage)},
            {'x': 5, 'y': decimal_default(sample.chr6_coverage)},
            {'x': 6, 'y': decimal_default(sample.chr7_coverage)},
            {'x': 8, 'y': decimal_default(sample.chr8_coverage)},
            {'x': 8, 'y': decimal_default(sample.chr9_coverage)},
            {'x': 9, 'y': decimal_default(sample.chr10_coverage)},
            {'x': 10, 'y': decimal_default(sample.chr11_coverage)},
            {'x': 11, 'y': decimal_default(sample.chr12_coverage)},
            {'x': 12, 'y': decimal_default(sample.chr13_coverage)},
            {'x': 13, 'y': decimal_default(sample.chr14_coverage)},
            {'x': 14, 'y': decimal_default(sample.chr15_coverage)},
            {'x': 15, 'y': decimal_default(sample.chr16_coverage)},
            {'x': 16, 'y': decimal_default(sample.chr17_coverage)},
            {'x': 17, 'y': decimal_default(sample.chr18_coverage)},
            {'x': 18, 'y': decimal_default(sample.chr19_coverage)},
            {'x': 19, 'y': decimal_default(sample.chr20_coverage)},
            {'x': 20, 'y': decimal_default(sample.chr21_coverage)},
            {'x': 21, 'y': decimal_default(sample.chr22_coverage)},
            {'x': 22, 'y': decimal_default(sample.chrx_coverage)}]} for sample in flowcell_run_data]#{'x': 23, 'y': decimal_default(sample.chry_coverage)}]} for sample in flowcell_run_data]

    context['data_coverate'] = coverage_data
    batch_data = {'13': {'data': {}, 'fields': ('flowcell_id', 'median_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'median_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'median_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'median_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'median_y')}}
    batch_data = extract_data(data=flowcell_data, info=batch_data, label=lambda x: "median", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
    context['median_coverage'] = [{"key": k, 'values': d['data']['median']} for k,d in batch_data.items()]

    ncd_batch_data = {'13': {'data': {}, 'fields': ('flowcell_id', 'ncd_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'ncd_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'ncd_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'ncd_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'ncd_y')}}
    control_type = SampleType.objects.get(name="Control")
    control_flowcell_data = BatchRun.objects.select_related().filter(sample_type=control_type).order_by('-flowcell_id__run_date')
    ncd_batch_data = extract_data(data=control_flowcell_data, info=ncd_batch_data, label=lambda x: "ncd", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
    context['ncd'] = [{"key": k, 'values': d['data']['ncd']} for k,d in batch_data.items()]
    samples_info_ff_formated = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info_ff_formated = extract_data(data=SamplesRunData.objects.all(), info=samples_info_ff_formated, label=lambda x: 'hist',x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
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
    #sample_flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell, sample_id=sample)
    flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell)#.exclude(sample_id=sample)
    samples_info = extract_data(SamplesRunData.objects.all().exclude(flowcell_id=flowcell), samples_info, size=0.5, label=lambda x: 'other', color="#bbdefb")#.get_samples_not_included(flowcell=flowcell,sample=sample), samples_info, label=lambda x: 'other')

    colors = ["#140c1c", "#442434", "#30346d", "#ffab40", "#854c30", "#346524", "#d04648", "#757161", "#597dce", "#d27d2c", "#8595a1", "#6daa2c", "#d2aa99", "#6dc2ca", "#dad45e", "#deeed6"]
    counter = 0
    shapes = ['diamond', 'square']
    color_dict = {}
    for sample in flowcell_run_data:
        samples_info = extract_data([sample], samples_info, label=lambda x: x.sample_id, size=1.0, shape="circle",color=colors[counter])
        color_dict[sample.sample_id] = color=colors[counter]
        counter = counter + 1
    #samples_info = extract_data(sample_flowcell_run_data, samples_info, label=lambda x: sample)
    data = {
             'today': datetime.date.today().strftime("%Y-%m-%d"),
             'sample': flowcell_run_data,
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
    samples_info = extract_data(flowcell_other, samples_info, size=0.5, label=lambda x: 'other', color="#bbdefb")
    #samples_info = extract_data(flowcell_run_data, samples_info, label=lambda x: barcode)

    colors = ["#140c1c", "#442434", "#30346d", "#ffab40", "#854c30", "#346524", "#d04648", "#757161", "#597dce", "#d27d2c", "#8595a1", "#6daa2c", "#d2aa99", "#6dc2ca", "#dad45e", "#deeed6"]
    counter = 0
    shapes = ['diamond', 'square']
    color_dict = {}
    for sample in flowcell_run_data:
        samples_info = extract_data([sample], samples_info, label=lambda x: x.sample_id, size=1.0, shape="circle",color=colors[counter])
        color_dict[sample.sample_id] = color=colors[counter]
        counter = counter + 1

    context = {'samples': [d.sample_id for d in flowcell_run_data], 'flowcell': barcode, 'flowcell_run_data': flowcell_run_data, 'color_dict': color_dict}
    context = data_structur_generator(samples_info, context)
    coverage_data =[{
            'key': sample.sample_id, 'values': [
            {'x': 1, 'y': decimal_default(sample.chr1_coverage)},
            {'x': 2, 'y': decimal_default(sample.chr2_coverage)},
            {'x': 3, 'y': decimal_default(sample.chr3_coverage)},
            {'x': 4, 'y': decimal_default(sample.chr4_coverage)},
            {'x': 5, 'y': decimal_default(sample.chr5_coverage)},
            {'x': 6, 'y': decimal_default(sample.chr6_coverage)},
            {'x': 7, 'y': decimal_default(sample.chr7_coverage)},
            {'x': 8, 'y': decimal_default(sample.chr8_coverage)},
            {'x': 9, 'y': decimal_default(sample.chr9_coverage)},
            {'x': 10, 'y': decimal_default(sample.chr10_coverage)},
            {'x': 11, 'y': decimal_default(sample.chr11_coverage)},
            {'x': 12, 'y': decimal_default(sample.chr12_coverage)},
            {'x': 13, 'y': decimal_default(sample.chr13_coverage)},
            {'x': 14, 'y': decimal_default(sample.chr14_coverage)},
            {'x': 15, 'y': decimal_default(sample.chr15_coverage)},
            {'x': 16, 'y': decimal_default(sample.chr16_coverage)},
            {'x': 17, 'y': decimal_default(sample.chr17_coverage)},
            {'x': 18, 'y': decimal_default(sample.chr18_coverage)},
            {'x': 19, 'y': decimal_default(sample.chr19_coverage)},
            {'x': 20, 'y': decimal_default(sample.chr20_coverage)},
            {'x': 21, 'y': decimal_default(sample.chr21_coverage)},
            {'x': 22, 'y': decimal_default(sample.chr22_coverage)},
            {'x': 23, 'y': decimal_default(sample.chrx_coverage)}]} for sample in flowcell_run_data]
            #{'x': 24, 'y': decimal_default(sample.chry_coverage)}]} for sample in flowcell_run_data]

    samples_info_ff_formated = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info_ff_formated = extract_data(flowcell_other, samples_info_ff_formated, lambda x: "hist",x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)

    samples_info_ff_formated = extract_data(flowcell_run_data, samples_info_ff_formated, lambda x: barcode,x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
    context = data_structur_generator(samples_info_ff_formated, context)
    context['data_coverage'] = coverage_data
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
