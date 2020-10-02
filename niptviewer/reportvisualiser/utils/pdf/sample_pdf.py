from wkhtmltopdf.views import PDFTemplateView
from dataprocessor.models import Flowcell, SamplesRunData
from reportvisualiser.utils.plots import extract_data, data_structur_generator
import datetime

class SampleReportPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'my_template.html'
    cmd_options = {
        'margin-top': 3,
        'javascript-delay': 2000,
        "no-stop-slow-scripts": True
    }
    def get_context_data(self, **kwargs):
        context = super(SampleReportPDF, self).get_context_data(**kwargs)
        samples_info = {'x_vs_y': {'data': {}, 'fields': ('ncv_X', 'ncv_Y')},
                   'x_vs_ff': {'data': {}, 'fields': ('ncv_X', 'ff_formatted')},
                   'y_vs_ff': {'data': {}, 'fields': ('ncv_Y', 'ff_formatted')},
                   'chr13_vs_ff': {'data': {}, 'fields': ('ncv_13', 'ff_formatted')},
                   'chr18_vs_ff': {'data': {}, 'fields': ('ncv_18', 'ff_formatted')},
                   'chr21_vs_ff': {'data': {}, 'fields': ('ncv_21', 'ff_formatted')}}
        flowcell = Flowcell.get_flowcell(flowcell_barcode=context['barcode'])
        sample_flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell, sample_id=context['sample'])
        flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell).exclude(sample_id=context['sample'])
        samples_info = extract_data('other', SamplesRunData.get_samples_not_included(flowcell=flowcell,sample=context['sample']), samples_info, only_prefix=True)

        samples_info = extract_data(context['barcode'], flowcell_run_data, samples_info, only_prefix=True)
        samples_info = extract_data(context['sample'], sample_flowcell_run_data, samples_info, only_prefix=True)
        context.update({
                 'today': datetime.date.today().strftime("%Y-%m-%d"),
                 'sample': context['sample'],
                 'flowcell_barcode': context['barcode'],
                 'run_date': flowcell.run_date.strftime("%Y-%m-%d")})
        context = data_structur_generator(samples_info, context)
        return context
