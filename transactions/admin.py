from django.contrib import admin
from .models import ImportProduct, ExportProduct,EmployeeWithdraw,Vacation

admin.site.register(ImportProduct)
admin.site.register(ExportProduct)
admin.site.register(EmployeeWithdraw)
admin.site.register(Vacation)

