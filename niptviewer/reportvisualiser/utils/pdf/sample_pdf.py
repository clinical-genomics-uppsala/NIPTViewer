from wkhtmltopdf.views import PDFTemplateView
from dataprocessor.models import Flowcell, SamplesRunData
from reportvisualiser.utils.plots import extract_data, data_structure_generator
from reportvisualiser.utils import colors, data
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import datetime
from dateutil.relativedelta import *


@method_decorator(login_required, name='dispatch')
class SampleReportPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'my_template.html'
    cmd_options = {
        'quiet': None,
        'enable-local-file-access': True,
        'margin-top': 3,
        "no-stop-slow-scripts": True,
        'debug-javascript': True,
    }

    def get_context_data(self, **kwargs):
        context = super(SampleReportPDF, self).get_context_data(**kwargs)
        self.filename = context['barcode'] + "_" + \
            datetime.date.today().strftime("%Y-%m-%d") + ".NIPT.pdf"

        flowcell = Flowcell.get_flowcell(flowcell_barcode=context['barcode'])

        previous_time = flowcell.run_date + relativedelta(months=-settings.DEFAULT_TIME_SELECTION_SAMPLE_REPORT)
        next_time = flowcell.run_date + relativedelta(months=+settings.DEFAULT_TIME_SELECTION_SAMPLE_REPORT)

        flowcell_run_data = SamplesRunData.objects.filter(flowcell_id=flowcell).select_related(). \
            values('sample_id', 'ff_formatted', 'ncv_13', 'ncv_18', 'ncv_21', 'ncv_X', 'ncv_Y')

        samples_run_data = SamplesRunData.get_samples(flowcell=flowcell)
        flowcell_other = SamplesRunData.get_samples_not_included(flowcell=flowcell, start_time=previous_time, stop_time=next_time)

        sample_info = data.extract_info_samples(flowcell_other, data.sample_info(), size=0.5, label=lambda x: 'other',
                                                color=colors.hist)
        color_dict, sample_info = data.extra_info_per_sample(samples_run_data, sample_info, label=lambda x: x['sample_id'],
                                                             size=1.0, shape="circle", colors=colors.samples)
        context.update(data_structure_generator(sample_info))

        qc_failure, qc_warning = data.extract_qc_status(samples_run_data)
        context['qc_warning'] = qc_warning
        context['qc_failure'] = qc_failure

        context.update({
             'today': datetime.date.today().strftime("%Y-%m-%d"),
             'samples': [d['sample_id'] for d in samples_run_data],
             'flowcell':  flowcell,
             'flowcell_run_data': flowcell_run_data,
             'flowcell_user': flowcell.uploading_user.first_name + " " + flowcell.uploading_user.last_name,
             'color_dict': color_dict,
             'flowcell_barcode': context['barcode'],
             'run_date': flowcell.run_date.strftime("%Y-%m-%d"),
             'upload_date': flowcell.created.strftime("%Y-%m-%d"),
             'page_type': "pdf"})

        return context
