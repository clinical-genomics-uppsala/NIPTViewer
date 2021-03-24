from . import views
from django.urls import re_path
from reportvisualiser.utils.pdf.sample_pdf import SampleReportPDF
from reportvisualiser.utils.pdf.qc_pdf import QCReportPDF
app_name = "viewer"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<active_page>[0-9]+)/(?P<time_selection>[0-9]+)m$', views.index, name='index'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})$', views.report, name='report'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})/(?P<time_selection>[0-9]+)m$', views.report, name='report'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})/(?P<sample>[A-Za-z0-9-]+)$', views.sample_report, name='sample_report'),
    re_path(r'^pdf/(?P<barcode>[A-Z0-9]{9})$',
            SampleReportPDF.as_view(template_name='reportvisualiser/sample_report.html'),
            name='sample_report_pdf'),
    re_path(r'^pdf/qc/(?P<barcode>[A-Z0-9]{9})$',
            QCReportPDF.as_view(template_name='reportvisualiser/qc_report.html'),
            name='qc_report_pdf'),
    re_path(r'^upload$', views.upload, name='upload'),
]
