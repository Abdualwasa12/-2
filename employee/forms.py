from django import forms
from .models import Employee

class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name']



    date_from = forms.DateField(label='Date From')
    amount = forms.IntegerField(label='Salary Amount')

    def __init__(self, *args, **kwargs):
        super(EmployeeSalaryForm, self).__init__(*args, **kwargs)
        self.fields['amount'].required = True  # Make the amount field required