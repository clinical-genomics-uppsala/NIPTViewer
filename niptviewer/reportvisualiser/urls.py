from django.urls import re_path

from . import views

app_name="viewer"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<barcode>[A-Z0-9]{9})$', views.report, name='report'),
    re_path(r'^upload$', views.upload, name='upload'),
]
