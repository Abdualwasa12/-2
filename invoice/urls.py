from django.urls import path
from . import views

app_name = 'invoice'

urlpatterns = [
    
    path('add_edit_import_invoice/', views.add_edit_import_invoice, name='add_edit_import_invoice'),
    path('add_edit_export_invoice/', views.add_edit_export_invoice, name='add_edit_export_invoice'),
    path('list_import_invoice/', views.list_import_invoice, name='list_import_invoice'),
    path('list_export_invoice/', views.list_export_invoice, name='list_export_invoice'),
    path('import_invoice_detail/<int:import_id>/',views.view_invoice_detail, name='import_invoice_detail'),
    path('export_invoice_detail/<int:export_id>/',views.view_invoice_detail, name='export_invoice_detail'),
]
