from .models import Flowcell, SamplesRunData

from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.http import HttpResponse
import csv

from .forms import UploadFileForm


@admin.register(Flowcell)
class FlowcellAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'run_date', 'flowcell_barcode']

    def import_flowcell_data(self, request):
        context = {}
        if request.method == 'POST':
            from .utils.data import import_flowcell_export
            if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    from io import TextIOWrapper
                    import_flowcell_export(TextIOWrapper(request.FILES['file'], "utf-8"))
                else:
                    context["form"] = form
            return redirect("admin:dataprocessor_flowcell_changelist")
        else:
            context["form"] = UploadFileForm()
        return TemplateResponse(request, "admin/dataprocessor/flowcell/upload.html", context)

    def export_flowcell_data(self, request):
        from .utils.data import export_flowcell_data
        response = HttpResponse(content_type='text/csv')
        from datetime import datetime
        response['Content-Disposition'] = 'attachment; filename="niptviewer_export.' + datetime.today().strftime('%Y-%m-%d') + '.csv"'
        writer = csv.writer(response)
        for data in export_flowcell_data():
            writer.writerow([data])
        return response

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("importdata/", self.import_flowcell_data), path("exportdata/", self.export_flowcell_data)]
        return my_urls + urls

admin.site.register(SamplesRunData)



