from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # Im
    path('import_product/', views.import_product, name='list_import_product'),
    path('add_edit_import_product/', views.add_edit_import_product, name='add_edit_import_product'),
    
    path('add_edit_import_product_j/<int:import_id>/', views.add_edit_import_product, name='edit_import'),
    path('add_edit_import_product_k/<int:dealer_id>/', views.add_edit_import_product, name='add_edit_import_product'),
    path('add_edit_import_product_m/<int:dealer_id>/<int:import_id>/', views.add_edit_import_product, name='add_edit_import_product'),
    path('delete_import_product/<int:id>',views.delete_import_product, name='delete_import_product'),
    path('generate_pdf_import/<int:dealer_id>', views.generate_pdf_import, name='generate_pdf_import'),
    
    # Ex
    path('export_product/', views.export_product, name='list_export_product'),
    path('add_edit_export_product/',views.add_edit_export_product, name='add_edit_export_product'),
    path('add_edit_export_product_j/<int:export_id>/',views.add_edit_export_product, name='add_edit_export_product'),
    path('delete_export_product/<int:id>',views.delete_export_product, name='delete_export_product'),
    path('generate_pdf_export/<int:dealer_id>', views.generate_pdf_export, name='generate_pdf_export'),
    
    
    
    # transactions by dealer
    path('imp_by_dealer/<int:dealer_id>',views.imp_by_dealer, name='imp_by_dealer'),
    path('exp_by_dealer/<int:dealer_id>',views.exp_by_dealer, name='exp_by_dealer'),
    
    
    # Withdraw
    path('withdraw/', views.withdraw, name='list_withdraw'),
    path('add_edit_employee_withdraw/',views.add_edit_employee_withdraw, name='add_edit_employee_withdraw'),
    path('add_edit_employee_withdraw_j/<int:withdraw_id>/',views.add_edit_employee_withdraw, name='add_edit_employee_withdraw'),
    path('add_edit_employee_withdraw_k/<int:employee_id>/',views.add_edit_employee_withdraw, name='add_edit_employee_withdraw_by_employee'),
    path('add_edit_employee_withdraw_m/<int:employee_id>/<int:withdraw_id>/',views.add_edit_employee_withdraw, name='add_edit_employee_withdraw'),
    path('delete_employee_withdraw/<int:emp_with_id>',views.delete_withdraw, name='delete_employee_withdraw'),
    path('generate_pdf_employee_withdraw/<int:employee_id>', views.generate_pdf_employee_withdraw, name='generate_pdf_employee_withdraw'),
    
    
    path('add_edit_dealer_withdraw/<int:dealer_id>/',views.add_edit_dealer_withdraw, name='add_edit_dealer_withdraw'),
    path('add_edit_dealer_withdraw/<int:dealer_id>/<int:withdraw_id>/',views.add_edit_dealer_withdraw, name='edit_dealer_withdraw'),
    path('delete_dealer_withdraw/<int:dea_with_id>',views.delete_withdraw, name='delete_dealer_withdraw'),
    path('generate_pdf_dealer_withdraw/<int:dealer_id>', views.generate_pdf_dealer_withdraw, name='generate_pdf_dealer_withdraw'),
    
    
    # Vacation
    path('vacation/', views.vacation, name='list_vacation'),
    path('add_edit_vacation/',views.add_edit_vacation, name='add_edit_vacation'),
    path('add_edit_vacation_main/<int:vacation_id>/',views.add_edit_vacation, name='add_edit_vacation_main'),
    path('add_edit_vacation_k/<int:employee_id>/',views.add_edit_vacation, name='add_edit_vacation'),
    path('add_edit_vacation_m/<int:employee_id>/<int:vacation_id>/',views.add_edit_vacation, name='add_edit_vacation'),
    path('delete_vacation/<int:id>',views.delete_vacation, name='delete_vacation'),
    path('generate_pdf_employee_vacation/<int:employee_id>', views.generate_pdf_employee_vacation, name='generate_pdf_employee_vacation'),
    
    
    
    # transactions by employee
    path('withdraw_by_employee/<int:employee_id>',views.withdraw_by_employee, name='withdraw_by_employee'),
    path('vacation_by_employee/<int:employee_id>',views.vacation_by_employee, name='vacation_by_employee'),
    
    path('withdraw_by_dealer/<int:dealer_id>',views.withdraw_by_dealer, name='withdraw_by_dealer'),
    
    

    
]