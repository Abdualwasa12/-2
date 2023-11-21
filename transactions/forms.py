from django import forms
from employee.models import Employee, OutEmployee
from .models import ImportProduct, ExportProduct,EmployeeWithdraw,DealerWithdraw,Vacation

from django import forms
from .models import ImportProduct



class ImportProductForm(forms.ModelForm):
    class Meta:
        model = ImportProduct
        fields = ['type_name','yard' ]
        widgets = {
  
            'type_name': forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'importproduct_type_name',
            'placeholder': 'نوع القماش',}),
            
            'yard': forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'importproduct_yard',
            'placeholder': '0',
            'type': 'number',
            }),
        }

    def __init__(self, *args, **kwargs):
            super(ImportProductForm, self).__init__(*args, **kwargs)

            # Make the "dealer" field read-only
            if 'initial' in kwargs and 'dealer' in kwargs['initial']:
                self.fields['dealer'].widget.attrs['readonly'] = True
                self.fields['dealer'].widget.attrs['disabled'] = True


class ExportProductForm(forms.ModelForm):
    class Meta:
        model = ExportProduct
        fields = ['product', 'type_name','price_of_one','quantity']
        widgets = {
       
            'product': forms.Select(attrs={
            'class': 'form-control',
            'id': 'exportproduct_product',
            'placeholder': 'سعر الحبة',
            'type': 'number',}),
      
            'type_name': forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'exportproduct_type_name',
            'placeholder': 'نوع العمل',}),
            
            'quantity': forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'exportproduct_quantity',
            'placeholder': 'العدد',
            'type': 'number',}),
            
            'price_of_one': forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'exportproduct_price_of_one',
            'placeholder': 'سعر الحبة',
            'type': 'number',}),
        }

    def __init__(self, *args, **kwargs):
        
        super(ExportProductForm, self).__init__(*args, **kwargs)

        # Customize the queryset for the 'product' field to only include products that belong to the current user
        existing_exported_products = ExportProduct.objects.all().values_list('product_id', flat=True)
        user_import_products = ImportProduct.objects.exclude(pk__in=existing_exported_products)
        self.fields['product'].queryset = user_import_products

        if 'instance' in kwargs:
            # If in edit mode, set the queryset for the 'product' field and make it readonly
            self.fields['product'].queryset = ImportProduct.objects.filter(pk=kwargs['instance'].product.pk)
            self.fields['product'].widget.attrs['readonly'] = True





class EmployeeWithdrawForm(forms.ModelForm):
    class Meta:
        model = EmployeeWithdraw
        fields = [ 'employee','date', 'withdraw', 'description',]
        widgets = {
            'employee': forms.Select(attrs={'class': 'employee-select'}),
        }
        
        
    def __init__(self,user, *args, **kwargs):
        super(EmployeeWithdrawForm, self).__init__(*args, **kwargs) 
                    # Adjust the queryset of the "dealer" field based on the current user
        self.fields['employee'].queryset = user.profile.employees.all()
        if 'initial' in kwargs and 'employee' in kwargs['initial']:
            self.fields['employee'].widget.attrs['readonly'] = True
            self.fields['employee'].widget.attrs['disabled'] = True
  

 
class DealerWithdrawForm(forms.ModelForm):
    class Meta:
        model = DealerWithdraw
        fields = [ 'dealer','date', 'withdraw', 'description',]
        widgets = {
            'dealer': forms.Select(attrs={'class': 'dealer-select'}),
        }
        
    def __init__(self, user, *args, **kwargs):
        super(DealerWithdrawForm, self).__init__(*args, **kwargs)
        self.fields['dealer'].queryset = user.profile.dealers.all()
        if 'initial' in kwargs and 'dealer' in kwargs['initial']:
            self.fields['dealer'].widget.attrs['readonly'] = True
            self.fields['dealer'].widget.attrs['disabled'] = True
        

class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = [ 'employee', 'type_vacation', 'date','description',]
        
    def __init__(self, user, *args, **kwargs):
        super(VacationForm,self).__init__(*args, **kwargs) 
        # Exclude employees in OutEmployee
        out_employee_ids = OutEmployee.objects.values_list('employee_id', flat=True)
        self.fields['employee'].queryset = Employee.objects.exclude(id__in=out_employee_ids)
        self.fields['employee'].queryset = user.profile.employees.exclude(id__in=out_employee_ids)
        if 'initial' in kwargs and 'employee' in kwargs['initial']:
            self.fields['employee'].widget.attrs['readonly'] = True
            self.fields['employee'].widget.attrs['disabled'] = True
            