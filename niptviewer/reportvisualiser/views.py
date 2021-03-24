from .forms import UploadFileForm
from .utils import plots, colors, data
from dataprocessor.models import Flowcell, SamplesRunData, BatchRun, SampleType
from dataprocessor.utils.data import import_data_into_database
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from reportvisualiser.utils.plots import data_structure_generator
import datetime
from dateutil.relativedelta import *
import math



@login_required
def index(request, active_page=1, time_selection="12"):
    """
            Information page showing flowcells that have been run and plot
            showing fetal fraction over time and NCV over time for controls
    """
    num_visible_flowcells = 10
    now = datetime.datetime.now()
    time_selection = int(time_selection)

    if time_selection == 9999:
        flowcells = Flowcell.objects.all()
        sample_run_data = SamplesRunData.objects.select_related().filter(flowcell_id__in=flowcells).order_by(
            '-flowcell_id__run_date')
        flowcell_run_data = BatchRun.objects.select_related().filter(flowcell_id__in=flowcells).order_by(
            '-flowcell_id__run_date')
    else:
        previous_time = now + relativedelta(months=-time_selection)
        flowcells = Flowcell.objects.filter(run_date__lte=now, run_date__gte=previous_time)
        sample_run_data = SamplesRunData.objects.select_related(). \
            filter(flowcell_id__in=flowcells).order_by('-flowcell_id__run_date')
        flowcell_run_data = BatchRun.objects.select_related().filter(flowcell_id__in=flowcells).order_by('-flowcell_id__run_date')

    control_type = SampleType.objects.get(name="Control")
    control_flowcell_data = SamplesRunData.objects.filter(flowcell_id__in=flowcells).select_related(). \
        filter(sample_type=control_type).order_by('-flowcell_id__run_date')

    num_flowcells = len(flowcells)
    active_page = int(active_page)
    context = {
               'flowcell_data': flowcell_run_data[(active_page-1)*num_visible_flowcells:active_page*num_visible_flowcells],
               "num_flowcells": num_flowcells,
               "num_pages": math.ceil(num_flowcells/num_visible_flowcells),
               "pages": range(1,math.ceil(num_flowcells/num_visible_flowcells)+1),
               "time_selection": time_selection,
               "active_page": active_page
    }

    if sample_run_data.exists():
        context['data_coverage'] = [plots.chromosome_coverage(data=sample_run_data)]
        context['data_ff_time'] = plots.fetal_fraction(data=sample_run_data)

    if control_flowcell_data.exists():
        context['ncd'] = plots.ncd_data(control_flowcell_data)

    template = loader.get_template("reportvisualiser/index.html")
    return HttpResponse(template.render(context, request))


@login_required
def sample_report(request, barcode, sample):
    flowcell = Flowcell.get_flowcell(flowcell_barcode=barcode)
    flowcell_run_data = SamplesRunData.objects. \
        filter(flowcell_id=flowcell).exclude(sample_id=sample)
    flowcell_controls = SamplesRunData.objects. \
        filter(flowcell_id=flowcell, sample_type=SampleType.objects.get(name="Control"))
    sample_run_data = SamplesRunData.objects. \
        filter(flowcell_id=flowcell, sample_id=sample)
    previous_samples = SamplesRunData.objects.all(). \
        exclude(flowcell_id=flowcell)

    samples_info = data.extract_info_samples(previous_samples, data.sample_info(), size=0.5, label=lambda x: 'other',
                                             color=colors.hist)
    samples_info = data.extract_info_samples(flowcell_run_data, samples_info, size=0.5, label=lambda x: 'same flowcell',
                                             color=colors.other_samples)
    color_dict, samples_info = data.extra_info_per_sample(sample_run_data, samples_info, label=lambda x: x.sample_id,
                                                          size=1.0, shape="circle", colors=[colors.sample])

    context = {'today': datetime.date.today().strftime("%Y-%m-%d"),
               'active_sample': sample,
               'samples': [d.sample_id for d in flowcell_run_data] + [sample_run_data[0].sample_id],
               'flowcell_barcode': barcode,
               'flowcell_run_data': sample_run_data,
               'flowcell_user': flowcell.uploading_user.first_name + " " + flowcell.uploading_user.last_name,
               'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
               'upload_date': flowcell.created.strftime("%Y-%m-%d"),
               'page_type': "html", 'color_dict': color_dict,
               'data_coverage_reads': plots.chromosome_percentage_reads(sample_run_data)}

    if sample_run_data.exists():
        context['data_coverage'] = plots.chromosome_coverage(data=sample_run_data) + plots.chromosome_coverage(
            data=flowcell_controls)
        context['data_ff_time'] = plots.fetal_fraction(data=previous_samples) + plots.fetal_fraction(
            data=flowcell_run_data, label=lambda x: barcode) + \
            plots.fetal_fraction(data=sample_run_data, label=lambda x: sample, size=2.0)

    qc_failure, qc_warning = data.extract_qc_status(sample_run_data)
    context['qc_warning'] = qc_warning
    context['qc_failure'] = qc_failure

    context.update(data_structure_generator(samples_info))
    template = loader.get_template("reportvisualiser/report.html")
    return HttpResponse(template.render(context, request))


@login_required
def report(request, barcode, time_selection="12"):
    time_selection = int(time_selection)
    flowcell = Flowcell.get_flowcell(flowcell_barcode=barcode)
    samples_run_data = SamplesRunData.get_samples(flowcell=flowcell)
    if time_selection == 9999:
        flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell)
    else:
        start_time = flowcell.run_date + relativedelta(months=-time_selection)
        stop_time = flowcell.run_date + relativedelta(months=+time_selection)
        flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell, start_time=start_time, stop_time=stop_time)

    sample_info = data.extract_info_samples(flowcell_other, data.sample_info(), size=0.5, label=lambda x: 'other',
                                            color=colors.hist)

    color_dict, sample_info = data.extra_info_per_sample(samples_run_data, sample_info, label=lambda x: x.sample_id,
                                                         size=1.0, shape="circle", colors=colors.samples)
    context = {
        'flowcell': flowcell,
        "time_selection": time_selection,
        'samples': [d.sample_id for d in samples_run_data],
        'flowcell_barcode': barcode,
        'flowcell_run_data': samples_run_data,
        'flowcell_user': flowcell.uploading_user.first_name + " " + flowcell.uploading_user.last_name,
        'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
        'upload_date': flowcell.created.strftime("%Y-%m-%d"),
        'color_dict': color_dict}
    context.update(data_structure_generator(sample_info))

    if samples_run_data.exists():
        context['data_coverage'] = plots.chromosome_coverage(data=samples_run_data)
        context['data_ff_time'] = plots.fetal_fraction(data=flowcell_other) + \
            plots.fetal_fraction(data=samples_run_data, label=lambda x: barcode)

    qc_failure, qc_warning = data.extract_qc_status(samples_run_data)
    context['qc_warning'] = qc_warning
    context['qc_failure'] = qc_failure

    context['data_coverage_reads'] = plots.chromosome_percentage_reads(samples_run_data)

    template = loader.get_template("reportvisualiser/report.html")
    return HttpResponse(template.render(context, request))


@login_required
def upload(request):
    context = {}
    template = loader.get_template("reportvisualiser/file_upload.html")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            flowcell = import_data_into_database(request.user, request.FILES['file'])
            if isinstance(flowcell, Flowcell):
                context['form_data'] = form
                context['file_validation'] = (flowcell.flowcell_barcode, flowcell.created)
                return HttpResponse(template.render(context, request))
            else:
                return redirect('viewer:report', barcode=flowcell)
        else:
            context['form_data'] = form
    else:
        context['form_data'] = UploadFileForm()
    return HttpResponse(template.render(context, request))
