from wkhtmltopdf.views import PDFTemplateView
from dataprocessor.models import Flowcell, SamplesRunData
from reportvisualiser.utils.plots import extract_data, data_structur_generator
import datetime

class SampleReportPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'my_template.html'
    cmd_options = {
        'margin-top': 3,
        #'javascript-delay': 2000,
        "no-stop-slow-scripts": True,
        'debug-javascript': True,
    }
    def get_context_data(self, **kwargs):
        context = super(SampleReportPDF, self).get_context_data(**kwargs)
        self.filename = context['barcode'] + "_" + datetime.date.today().strftime("%Y-%m-%d") +".NIPT.pdf"
        samples_info = {'x_vs_y': {'data': {}, 'fields': ('ncv_X', 'ncv_Y')},
                   'x_vs_ff': {'data': {}, 'fields': ('ncv_X', 'ff_formatted')},
                   'y_vs_ff': {'data': {}, 'fields': ('ncv_Y', 'ff_formatted')},
                   'chr13_vs_ff': {'data': {}, 'fields': ('ncv_13', 'ff_formatted')},
                   'chr18_vs_ff': {'data': {}, 'fields': ('ncv_18', 'ff_formatted')},
                   'chr21_vs_ff': {'data': {}, 'fields': ('ncv_21', 'ff_formatted')}}
        flowcell = Flowcell.get_flowcell(flowcell_barcode=context['barcode'])
        #sample_flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell, sample_id=context['sample'])
        flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell)#.exclude(sample_id=context['sample'])
        color_dict = {}
        samples_info = extract_data(SamplesRunData.objects.all().exclude(flowcell_id=flowcell), samples_info,size=0.5, label=lambda x: 'other', color="#bbdefb")
        #.get_samples_not_included(flowcell=flowcell,sample=context['sample']), samples_info, label=lambda x: 'other')
        #colors = ["#191970", "#006400", "#ff0000", "#ffca28", "#00ff00", "#00ffff", "#ff00ff", "#ffb6c1"]
        colors = ["#140c1c", "#442434", "#30346d", "#ffab40", "#854c30", "#346524", "#d04648", "#757161", "#597dce", "#d27d2c", "#8595a1", "#6daa2c", "#d2aa99", "#6dc2ca", "#dad45e", "#deeed6"]
        counter = 0
        shapes = ['diamond', 'square']
        for sample in flowcell_run_data:
            samples_info = extract_data([sample], samples_info, label=lambda x: x.sample_id, size=1, shape="circle",color=colors[counter])
            color_dict[sample.sample_id] = color=colors[counter]
            counter = counter + 1

        #samples_info = extract_data(sample_flowcell_run_data, samples_info, label=lambda x: context['sample'], shape='cross',size=10)
        context.update({
                 'today': datetime.date.today().strftime("%Y-%m-%d"),
                 'flowcell_run_data': flowcell_run_data,
                 'color_dict': color_dict,
                 'flowcell_barcode': context['barcode'],
                 'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
                 'page_type': "pdf"})
        context.update(data_structur_generator(samples_info))
        return context
