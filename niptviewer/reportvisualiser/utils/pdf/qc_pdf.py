from dataprocessor.models import Flowcell, SamplesRunData, BatchRun, SampleType
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reportvisualiser.utils import plots
from reportvisualiser.utils import colors, data
from wkhtmltopdf.views import PDFTemplateView

import datetime
from dateutil.relativedelta import *


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
        self.filename = context['barcode'] + "_" + datetime.date.today().strftime("%Y-%m-%d") + ".QC.NIPT.pdf"

        flowcell = Flowcell.get_flowcell(flowcell_barcode=context['barcode'])

        previous_time = flowcell.run_date + relativedelta(months=-settings.DEFAULT_TIME_SELECTION_QC_REPORT)
        next_time = flowcell.run_date + relativedelta(months=+settings.DEFAULT_TIME_SELECTION_QC_REPORT)

        samples_run_data = SamplesRunData.get_samples(flowcell=flowcell)
        flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell, start_time=previous_time, stop_time=next_time)

        qc_failure, qc_warning = data.extract_qc_status(samples_run_data)
        context['qc_warning'] = qc_warning
        context['qc_failure'] = qc_failure

        control_type = SampleType.objects.get(name="Control")
        control_other_flowcell_data = SamplesRunData.objects. \
            filter(sample_type=control_type, flowcell_id__run_date__gte=previous_time, flowcell_id__run_date__lte=next_time). \
            exclude(flowcell_id=flowcell).order_by('-flowcell_id__run_date').select_related(). \
            values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode', 'sample_id', 'sample_type__name',
                   'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y', 'ncd_13', 'ncd_18', 'ncd_21', 'ncd_x', 'ncd_y',
                   'chr1_coverage', 'chr2_coverage', 'chr3_coverage', 'chr4_coverage', 'chr5_coverage', 'chr6_coverage',
                   'chr7_coverage', 'chr8_coverage', 'chr9_coverage', 'chr10_coverage', 'chr11_coverage', 'chr12_coverage',
                   'chr13_coverage', 'chr14_coverage', 'chr15_coverage', 'chr16_coverage', 'chr17_coverage', 'chr18_coverage',
                   'chr19_coverage', 'chr20_coverage', 'chr21_coverage', 'chr22_coverage', 'chrx_coverage', 'chry_coverage',
                   'qc_flag', 'qc_failure', 'qc_warning',  'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8',
                   'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20',
                   'chr21', 'chr22', 'Chrx', 'chry')
        control_flowcell_data = SamplesRunData.objects. \
            filter(sample_type=control_type, flowcell_id=flowcell, flowcell_id__run_date__gte=previous_time,
                   flowcell_id__run_date__lte=next_time).select_related(). \
            values('ff_formatted', 'flowcell_id__run_date', 'flowcell_id__flowcell_barcode', 'sample_id',
                   'sample_type__name', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y', 'ncd_13', 'ncd_18', 'ncd_21',
                   'ncd_x', 'ncd_y', 'chr1_coverage', 'chr2_coverage', 'chr3_coverage', 'chr4_coverage', 'chr5_coverage',
                   'chr6_coverage', 'chr7_coverage', 'chr8_coverage', 'chr9_coverage', 'chr10_coverage', 'chr11_coverage',
                   'chr12_coverage', 'chr13_coverage', 'chr14_coverage', 'chr15_coverage', 'chr16_coverage',
                   'chr17_coverage', 'chr18_coverage', 'chr19_coverage', 'chr20_coverage', 'chr21_coverage',
                   'chr22_coverage', 'chrx_coverage', 'chry_coverage', 'qc_flag', 'qc_failure', 'qc_warning',
                   'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12',
                   'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'Chrx',
                   'chry')
        if control_flowcell_data.exists():
            context['ncd'] = plots.ncd_data(control_flowcell_data, context['barcode'], size=1.0)
            if control_other_flowcell_data.exists():
                context['ncd'] = plots.ncd_data(control_other_flowcell_data, "other", size=0.5) + context['ncd']
        if samples_run_data.exists():
            context['data_coverage'] = plots.chromosome_coverage(data=samples_run_data)
            current_fetal = plots.fetal_fraction(data=samples_run_data, label=lambda x: context['barcode'])
            context['data_ff_time'] = current_fetal['data_ff_time']
            context['data_ff_time_min_x'] = current_fetal['data_ff_time_min_x']
            context['data_ff_time_min_y'] = current_fetal['data_ff_time_min_y']
            context['data_ff_time_max_x'] = current_fetal['data_ff_time_max_x']
            context['data_ff_time_max_y'] = current_fetal['data_ff_time_max_y']

            if flowcell_other.exists():
                other_fetal = plots.fetal_fraction(data=flowcell_other, label=lambda x: "other")
                context['data_ff_time'] = other_fetal['data_ff_time'] + context['data_ff_time']
                context['data_ff_time_min_x'] = min(other_fetal['data_ff_time_min_x'], context['data_ff_time_min_x'])
                context['data_ff_time_min_y'] = min(other_fetal['data_ff_time_min_y'], context['data_ff_time_min_y'])
                context['data_ff_time_max_x'] = max(other_fetal['data_ff_time_max_x'], context['data_ff_time_max_x'])
                context['data_ff_time_max_y'] = max(other_fetal['data_ff_time_max_y'], context['data_ff_time_max_y'])
            context['data_coverage_reads'] = plots.chromosome_percentage_reads(samples_run_data)

        context.update({
            'today': datetime.date.today().strftime("%Y-%m-%d"),
            'flowcell': flowcell,
            'flowcell_user': flowcell.uploading_user.first_name + " " + flowcell.uploading_user.last_name,
            'flowcell_barcode': context['barcode'],
            'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
            'upload_date': flowcell.created.strftime("%Y-%m-%d"),
            'page_type': "pdf"})

        return context
