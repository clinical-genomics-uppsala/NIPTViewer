from django.urls import re_path

from . import views
from reportvisualiser.utils.pdf.sample_pdf import SampleReportPDF
app_name="viewer"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})$', views.report, name='report'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})/(?P<sample>[A-Z0-9-]+)$', views.sample_report, name='sample_report'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})/(?P<sample>[A-Z0-9-]+)/pdf$', SampleReportPDF.as_view(template_name='reportvisualiser/sample_report.html', filename='sample_report.pdf'), name='sample_report_pdf'),
    re_path(r'^upload$', views.upload, name='upload'),
]
