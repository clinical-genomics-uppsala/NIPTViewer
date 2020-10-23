
from django.http import HttpResponse
from django.template import loader
from dataprocessor.models import BatchRun, Flowcell, SamplesRunData, SampleType
from reportvisualiser.utils.plots import extract_data, data_structur_generator

def index(request):
    num_flowcells = Flowcell.objects.count()
    num_samples = SamplesRunData.objects.count()
    batch_data = BatchRun.objects.all()
    latest_flowcells = Flowcell.objects.all().order_by('-run_date')[:5]
    latest_samples = SamplesRunData.objects.all().order_by('-flowcell_id__run_date')[:5]
    samples_info = {'ff_time': {'data': {}, 'fields': ('flowcell_id', 'ff_formatted')}}
    samples_info = extract_data(data=SamplesRunData.objects.all(), info=samples_info, label = lambda x: 'hist', x_format= lambda x: getattr(x, 'run_date').timestamp()*1000)
    context = {'num_flowcells': num_flowcells, 'num_samples': num_samples, 'latest_flowcells': latest_flowcells,'latest_samples': latest_samples}
    batch_info = {'13': {'data': {}, 'fields': ('flowcell_id', 'median_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'median_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'median_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'median_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'median_y')}}

    if batch_data.exists():
        batch_data = extract_data(data=batch_data, info=batch_info, label=lambda x: "median", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
        context['median_coverage'] = [{"key": k, 'values': d['data']['median']} for k,d in batch_data.items()]

        ncd_batch_data = {'13': {'data': {}, 'fields': ('flowcell_id', 'ncd_13')},
                  '18': {'data': {}, 'fields': ('flowcell_id', 'ncd_18')},
                  '21': {'data': {}, 'fields': ('flowcell_id', 'ncd_21')},
                  'x': {'data': {}, 'fields': ('flowcell_id', 'ncd_x')},
                  'y': {'data': {}, 'fields': ('flowcell_id', 'ncd_y')}}


    control_type = SampleType.objects.get(name="Control")
    control_flowcell_data = SamplesRunData.objects.select_related().filter(sample_type=control_type).order_by('-flowcell_id__run_date')
    if control_flowcell_data.exists():
        ncd_batch_data = extract_data(data=control_flowcell_data, info=ncd_batch_data, label=lambda x: "ncd", x_format= lambda x: getattr(x, 'run_date').timestamp()*1000, extra_info=lambda x: {'label': x.flowcell_id.flowcell_barcode})
        context['ncd'] = [{"key": k, 'values': d['data']['ncd']} for k,d in ncd_batch_data.items()]

    context = data_structur_generator(samples_info, context)
    template = loader.get_template("base.html")
    return HttpResponse(template.render(context, request))
