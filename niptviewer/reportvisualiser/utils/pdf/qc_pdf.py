from wkhtmltopdf.views import PDFTemplateView
from dataprocessor.models import Flowcell, SamplesRunData
from reportvisualiser.utils import plots
from reportvisualiser.utils import colors, data

import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from dataprocessor.models import Flowcell, SamplesRunData, BatchRun, SampleType

@method_decorator(login_required, name='dispatch')
class QCReportPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'my_template.html'
    cmd_options = {
        'quiet': None,
        'enable-local-file-access': True,
        'margin-top': 3,
        'javascript-delay': 2000,
        "no-stop-slow-scripts": True,
        'debug-javascript': True,
    }

    def get_context_data(self, **kwargs):
        context = super(QCReportPDF, self).get_context_data(**kwargs)
        self.filename = context['barcode'] + "_" + datetime.date.today().strftime("%Y-%m-%d") +".QC.NIPT.pdf"

        flowcell = Flowcell.get_flowcell(flowcell_barcode=context['barcode'])
        flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell)

        samples_run_data = SamplesRunData.get_samples(flowcell=flowcell)
        flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell)

        qc_failure, qc_warning = data.extract_qc_status(samples_run_data)
        context['qc_warning'] = qc_warning
        context['qc_failure'] = qc_failure

        control_type = SampleType.objects.get(name="Control")
        control_other_flowcell_data = SamplesRunData.objects.select_related().filter(sample_type=control_type).exclude(flowcell_id=flowcell).order_by('-flowcell_id__run_date')
        control_flowcell_data = SamplesRunData.objects.select_related().filter(sample_type=control_type,flowcell_id=flowcell)
        if control_flowcell_data.exists():
            context['ncd'] = plots.ncd_data(control_flowcell_data, context['barcode'], size=1.0)
            if control_other_flowcell_data.exists():
                context['ncd'] = plots.ncd_data(control_other_flowcell_data, "other", size=0.5) + context['ncd']

        if samples_run_data.exists():
            context['data_coverage'] = plots.chromosome_coverage(data=samples_run_data)
            context['data_ff_time'] = plots.fetal_fraction(data=samples_run_data, label=lambda x: context['barcode'])
            if flowcell_other.exists():
                context['data_ff_time'] = plots.fetal_fraction(data=flowcell_other, label=lambda x: "other") + context['data_ff_time']
            context['data_coverage_reads'] = plots.chromosome_percentage_reads(samples_run_data)

        context.update({
                 'today': datetime.date.today().strftime("%Y-%m-%d"),
                 'flowcell':  flowcell,
                 'flowcell_user': flowcell.uploading_user.first_name + " " + flowcell.uploading_user.last_name,
                 'flowcell_barcode': context['barcode'],
                 'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
                 'upload_date': flowcell.created.strftime("%Y-%m-%d"),
                 'page_type': "pdf"})

        return context
