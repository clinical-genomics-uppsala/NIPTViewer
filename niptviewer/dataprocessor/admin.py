from .models import Flowcell, SamplesRunData
from django.contrib import admin


@admin.register(Flowcell)
class FlowcellAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'run_date', 'flowcell_barcode']


admin.site.register(SamplesRunData)
