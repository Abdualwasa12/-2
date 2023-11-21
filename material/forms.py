from django import forms
from .models import Material
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [ 'dealer','name','quantity', 'price','date','num_of_bill', 'description',]
        