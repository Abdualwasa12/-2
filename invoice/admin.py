from django.contrib import admin
from .models import ExportInvoice, ImportInvoice, ExportInvoiceDetail, ImportInvoiceDetail
# Register your models here.

admin.site.register(ExportInvoiceDetail)
admin.site.register(ImportInvoiceDetail)

class ImportInvoiceDetailInline(admin.TabularInline):
    model = ImportInvoiceDetail
    fields = ('import_product',)
    readonly_fields = ('import_product',)
    extra = 0

class ImportInvoiceAdmin(admin.ModelAdmin):
    list_display = ('dealer', 'date', 'total_yards')
    inlines = [ImportInvoiceDetailInline]

    def total_yards(self, obj):
        return obj.total_yards()
    total_yards.short_description = 'Total Yards'

admin.site.register(ImportInvoice, ImportInvoiceAdmin)


class ExportInvoiceDetailInline(admin.TabularInline):
    model = ExportInvoiceDetail
    fields = ('export_product',)
    readonly_fields = ('export_product',)
    extra = 0

@admin.register(ExportInvoice)
class ExportInvoiceAdmin(admin.ModelAdmin):
    inlines = [ExportInvoiceDetailInline]
    list_display = ('dealer', 'description', 'date', 'total_invoice_price')  # Add any fields you want to display

    def total_invoice_price(self, obj):
        total_price = 0
        for detail in obj.exportinvoicedetail_set.all():
            total_price += detail.export_product.total_price()
        return total_price

    total_invoice_price.short_description ='Total Invoice' 