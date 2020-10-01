from django.contrib import admin

# Register your models here.

from .models import Flowcell, SamplesRunData

@admin.register(Flowcell)
class FlowcellAdmin(admin.ModelAdmin):
    readonly_fields=['created', 'run_date','flowcell_barcode']

admin.site.register(SamplesRunData)
