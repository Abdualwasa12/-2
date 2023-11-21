from django.urls import path
from . import views

app_name = 'material'

urlpatterns = [
    path('',views.material, name='material'),
    path('add_edit_material/',views.add_edit_dealer_material, name='add_edit_material' ),
    path('add_edit_material/<int:material_id>',views.add_edit_dealer_material, name='add_edit_material' ),
    path('delete_material/<int:id>',views.delete_material, name='delete_material' ),
    path('material_by_dealer/<int:dealer_id>',views.material_by_dealer, name='material_by_dealer'),
    path('generate_pdf_dealer_materail/<int:dealer_id>', views.generate_pdf_dealer_materail, name='generate_pdf_dealer_materail'),
]