from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.employee, name='list_employee'),
    path('add_edit_employee/',views.add_edit_employee, name='add_edit_employee'),
    path('add_edit_employee/<int:employee_id>',views.add_edit_employee, name='add_edit_employee'),
    path('delete_employee/<int:id>',views.delete_employee, name='delete_employee'),
    
    # Detail
    path('detail_employee/<int:employee_id>',views.detail_employee, name='detail_employee'),

    # Out Employee
    path('out_employee/', views.out_employee, name='list_out_employee'),
    path('add_employee_to_out/<int:employee_id>/', views.add_employee_to_out, name='add_employee_to_out'),

]