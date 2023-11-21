from django.urls import path
from . import views

app_name = 'dealer'

urlpatterns = [
    path('', views.dealer, name='list_dealer'),
    path('add_edit_dealer/',views.add_edit_dealer, name='add_edit_dealer'),
    path('add_edit_dealer/<int:dealer_id>',views.add_edit_dealer, name='add_edit_dealer'),
    path('delete_dealer/<int:id>',views.delete_dealer, name='delete_dealer'),
    
    # Detail
    path('detail_dealer/<int:dealer_id>',views.detail_dealer, name='detail_dealer'),
    
]