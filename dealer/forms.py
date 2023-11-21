from django import forms
from .models import Dealer
from django.forms import formset_factory

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['name']
        
        
