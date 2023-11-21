
from django import forms
from .models import ImportInvoice,ExportInvoice
class ImInvoiceForm(forms.ModelForm):
    class Meta:
        model = ImportInvoice
        fields = [
            'dealer',
            'description',
            'date',
        ]
        widgets ={
            
            
             'dealer': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_dealer',
                'placeholder': 'التاجر',}),
            
             'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_description',
                'placeholder': 'التفاصيل',}),
             
             'date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'invoice_date',
                'placeholder': 'التاريخ',}),
        }
         
    def __init__(self,user, *args, **kwargs):
        super(ImInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['dealer'].queryset = user.profile.dealers.all()
        
class ExInvoiceForm(forms.ModelForm):
    class Meta:
        model = ExportInvoice
        fields = [
            'dealer',
            'description',
            'date',
        ]
        widgets ={
            
             'dealer': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_dealer',
                'placeholder': 'التاجر',}),
            
             'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_description',
                'placeholder': 'التفاصيل',}),
             
             'date': forms.SelectDateWidget(attrs={
                'class': 'form-control-inline',  # Adjust the class name for inline display
                'id': 'invoice_date',
                'placeholder': 'التاريخ',}),
        }
    def __init__(self,user, *args, **kwargs):
        super(ExInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['dealer'].queryset = user.profile.dealers.all()
        
        


