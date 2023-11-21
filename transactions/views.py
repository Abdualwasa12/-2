from django.shortcuts import get_object_or_404, redirect, render
from dealer.models import Dealer
from invoice.models import ImportInvoice
from .models import ImportProduct, ExportProduct,EmployeeWithdraw,DealerWithdraw,Vacation
from django.contrib import messages
from .forms import  ExportProductForm, ImportProductForm,EmployeeWithdrawForm,DealerWithdrawForm, VacationForm
from employee.models import Employee
from employee.views import calculate_totals# The above code is importing the `calculate_totals`
# function from the `dealer.views` module and renaming it
# as `dealer_calcula`.
from dealer.views import calculate_totals as dealer_calculate_totals
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
from django_htmx.http import HttpResponseClientRedirect
from django.db.models import F
# Create your views here.

def import_product(request):

    current_user = request.user.profile
    import_products = ImportProduct.objects.filter(importinvoicedetail__invoice__dealer__user=current_user).annotate(
        dealer_name=F('importinvoicedetail__invoice__dealer__name'),
        date=F('importinvoicedetail__invoice__date'))
    return render(request, 'import/list_import_product.html', {'import_products': import_products})

def add_edit_import_product(request, dealer_id=None, import_id=None):
    user = request.user
    if dealer_id:
        dealer = get_object_or_404(Dealer, id=dealer_id ,user=request.user.profile)  
        form = ImportProductForm(user,request.POST or None, initial={'dealer': dealer})

    else:
        form = ImportProductForm(user,request.POST or None)
               
    if import_id:
        import_instance = get_object_or_404(ImportProduct, id=import_id,user=request.user.profile)
        form = ImportProductForm(user,request.POST or None, instance=import_instance)
        if dealer_id:
            form = ImportProductForm(user,request.POST or None, instance=import_instance, initial={'dealer': dealer})
    if request.method == 'POST':
        if form.is_valid():
            if dealer_id:
                form.instance.dealer = dealer
            form.save()
            messages.success(request, 'تم اضافة المنتج بنجاح')
            return redirect('transactions:list_import_product')

    return render(request, 'import/add_edit_import_product.html', {'form': form})



def delete_import_product(request, id ):
    product =get_object_or_404(ImportProduct, id=id)
    if product.dealer.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this vacation")
    if request.method == 'POST':
        product.delete()
        messages.success(request,'تم حذف المنتج بنجاح')
        return redirect('transactions:list_import_product')
    return render(request, 'import/delete_import_product.html')



 ################## Export Product #################




def export_product(request):
    current_user = request.user.profile
    export_products = ExportProduct.objects.filter(exportinvoicedetail__invoice__dealer__user=current_user)
    return render(request, 'export/list_export_product.html', {'export_products': export_products})

def add_edit_export_product(request, export_id=None):
    current_user = request.user.profile
    if export_id:
        export_instance = get_object_or_404(ExportProduct, pk=export_id)
        form = ExportProductForm(request.POST or None, instance=export_instance, current_user=current_user, initial={'product': export_instance.product})
        if export_instance.product.dealer.user != current_user:
            return HttpResponseForbidden("You are not authorized to access this resource")
    else:
        form = ExportProductForm(request.POST or None, current_user=current_user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
        messages.success(request, 'تم اضافة المنتج بنجاح')
        return redirect('transactions:list_export_product')

    return render(request, 'export/add_edit_export_product.html', {'form': form})



def delete_export_product(request, id ):
    product1 =get_object_or_404(ExportProduct, id=id)
    if product1.product.dealer.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this vacdation")
    if request.method == 'POST':
        product1.delete()
        messages.success(request,'تم حذف المنتج بنجاح')
        return redirect('transactions:list_export_product')
    return render(request, 'export/delete_export_product.html')


################ Specfic Dealer ################

def imp_by_dealer(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id, user=request.user.profile)
    import_products = ImportProduct.objects.filter(importinvoicedetail__invoice__dealer=dealer)
    return render(request, 'import/imp_by_dealer.html', {'import_products': import_products,'dealer':dealer})




def exp_by_dealer(request, dealer_id):
    dealer =Dealer.objects.get(id=dealer_id,user=request.user.profile)
    export_products = ExportProduct.objects.filter(exportinvoicedetail__invoice__dealer=dealer)
    return render(request, 'export/exp_by_dealer.html', {'export_products': export_products,'dealer':dealer})


############### Employee ################

def withdraw(request):
    current_user = request.user.profile
    employees = Employee.objects.filter(user=current_user)
    withdraws = EmployeeWithdraw.objects.filter(employee__in=employees)
    return render(request, 'withdraw/list_withdraw.html', {'withdraws': withdraws})


def add_edit_employee_withdraw(request, employee_id=None, withdraw_id=None ):
    user = request.user
    if employee_id:
        employee = get_object_or_404(Employee, id=employee_id,user= request.user.profile)  
        form = EmployeeWithdrawForm(user,request.POST or None,initial={'employee': employee})

    else:
        form = EmployeeWithdrawForm(user,request.POST or None)
        
    if withdraw_id:
        withdraw_instance = get_object_or_404(EmployeeWithdraw, id=withdraw_id,user= request.user.profile)
        form = EmployeeWithdrawForm(user,request.POST or None, instance=withdraw_instance)
        
        if employee_id:
            form = EmployeeWithdrawForm(user,request.POST or None, instance=withdraw_instance,initial={'employee': employee}) 

    if request.method == 'POST':
        if form.is_valid():
            if employee_id:
                form.instance.employee = employee
            form.save()
        messages.success(request,'تم اضافة معلومات العميل بنجاح')
        if request.htmx:
            return HttpResponseClientRedirect("/transactions/withdraw/")
        return redirect('transactions:list_withdraw')
    return render(request , 'withdraw/add_edit_withdraw.html', {'form':form})


def delete_withdraw(request, dea_with_id=None, emp_with_id=None ):
    if emp_with_id:
        withdraw =get_object_or_404(EmployeeWithdraw, id=emp_with_id)
        if withdraw.employee.user != request.user.profile:
            return HttpResponseForbidden("You are not authorized to delete this vacation")
    if dea_with_id:
        withdraw =get_object_or_404(DealerWithdraw, id=dea_with_id)
        if withdraw.dealer.user != request.user.profile:
            return HttpResponseForbidden("You are not authorized to delete this vacation")
    if request.method == 'POST':
        withdraw.delete()
        messages.success(request,'تم حذف معلومات العميل بنجاح')
        return redirect('transactions:list_withdraw')
    return render(request, 'withdraw/delete_withdraw.html')


############### Vacation ################


    current_user = request.user.profile
def vacation(request):
    current_user = request.user.profile
    employees = Employee.objects.filter(user=current_user)
    vacations = Vacation.objects.filter(employee__in=employees)
    return render(request, 'vacation/list_vacation.html', {'vacations': vacations})


@login_required
def add_edit_vacation(request, vacation_id=None, employee_id=None):
    current_user = request.user.profile
    user = request.user
    
    if employee_id:
        employee = get_object_or_404(Employee, id=employee_id, user=current_user)
        form = VacationForm(user,request.POST or None, initial={'employee': employee})
    else:
        form = VacationForm(user,request.POST or None)

    if vacation_id:
        vacation_instance = get_object_or_404(Vacation, id=vacation_id, user=current_user)
        form = VacationForm(user,request.POST or None, instance=vacation_instance)
        if employee_id:
            form = VacationForm(user,request.POST or None, instance=vacation_instance, initial={'employee': employee})

    if request.method == 'POST':
        if form.is_valid():
            if employee_id:
                form.instance.employee = employee
            form.save()
            messages.success(request, 'تم اضافة معلومات العميل بنجاح')
            if request.htmx:
                return HttpResponseClientRedirect("/transactions/vacation/")
            return redirect('transactions:list_vacation')
            

    return render(request, 'vacation/add_edit_vacation.html', {'form': form})




def delete_vacation(request, id):
    vacation = get_object_or_404(Vacation, id=id)
    
    # Check if the vacation belongs to the current user
    if vacation.employee.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this vacation")
    
    if request.method == 'POST':
        vacation.delete()
        messages.success(request, 'تم حذف معلومات الإجازة بنجاح')
        return redirect('transactions:list_vacation')
    
    return render(request, 'vacation/delete_vacation.html')



############### Dealer Withdraw ##################

def add_edit_dealer_withdraw(request, withdraw_id=None, dealer_id=None):
    current_user= request.user.profile
    user = request.user

    if dealer_id:
        dealer = get_object_or_404(Dealer, id=dealer_id)  
        form = DealerWithdrawForm(user,request.POST or None,initial={'dealer': dealer})
        if dealer.user != current_user:
            return HttpResponseForbidden("You are not authorized to access this resource")
        if withdraw_id:
            withdraw_instance = get_object_or_404(DealerWithdraw, pk=withdraw_id,user=current_user)
            form = DealerWithdrawForm(user,request.POST or None, instance=withdraw_instance,initial={'dealer': dealer})

    else:
        form = DealerWithdrawForm(user,request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if dealer_id:
                i = form.save(commit=False)
                i.dealer = dealer
            form.save()
            messages.success(request, 'تم حفظ معلومات العميل بنجاح')
            if request.htmx:
                return HttpResponseClientRedirect("/dealer/")
            return redirect('transactions:list_withdraw')

    return render(request, 'withdraw/add_edit_withdraw.html', {'form': form})

############### Specific Employee ################

def withdraw_by_employee(request, employee_id):
    current_user = request.user.profile
    employees = Employee.objects.filter(user=current_user)
    employee = get_object_or_404(Employee, id=employee_id)
    withdraws = EmployeeWithdraw.objects.filter(employee__in=employees).filter(employee=employee)
    
    # calculate the vacation
    employee_totals = calculate_totals(employee_id)
    total_withdrawals = employee_totals['total_withdrawals']
    
    return render(request, 'withdraw/withdraw_by_employee.html', {'withdraws': withdraws,
                                                                  'employee':employee,
                                                                  'total_withdrawals':total_withdrawals})

def vacation_by_employee(request, employee_id):
    current_user = request.user.profile
    employees = Employee.objects.filter(user=current_user)
    employee = get_object_or_404(Employee, id =employee_id)
    vacations = Vacation.objects.filter(employee__in=employees).filter(employee=employee)
    
    employee_totals = calculate_totals(employee_id)
    total_vacation =employee_totals.get('total_amount_vacation')
    return render(request, 'vacation/vacation_by_employee.html', {'vacations': vacations,
                                                                  'employee':employee,
                                                                  'total_vacation':total_vacation})


############### Specific Dealer ################

def withdraw_by_dealer(request, dealer_id):
    current_user = request.user.profile
    dealers = Dealer.objects.filter(user=current_user)
    dealer = get_object_or_404(Dealer, id=dealer_id)
    withdraws = DealerWithdraw.objects.filter(dealer__in=dealers).filter(dealer=dealer)
    dealer_total = dealer_calculate_totals(dealer_id)
    total_withdrawals = dealer_total['total_dealer_withdrawals']
    total_dealer_materials = dealer_total['total_dealer_materials']
    return render(request, 'withdraw/withdraw_by_dealer.html',{ 'withdraws': withdraws,'dealer':dealer,'total_withdrawals':total_withdrawals,'total_dealer_materials':total_dealer_materials})




#################### PDF ###################

def generate_pdf_import(request, dealer_id):

       # Get the products data that you want to display in the PDF
       dealer = get_object_or_404(Dealer, id=dealer_id)
       products = ImportProduct.objects.filter(dealer=dealer)

       # Load the HTML template
       template = get_template('import/pdf_template.html')

       # Context data for rendering the template
       context = {'import_products': products,
                  'dealer': dealer}

       # Render the HTML template with the context data
       html_string = template.render(context)

       # Create a PDF document using WeasyPrint
       html = HTML(string=html_string)
       pdf_file = html.write_pdf()

       # Create an HTTP response with the PDF content
       response = HttpResponse(pdf_file, content_type='application/pdf')
       response['Content-Disposition'] = 'filename="import_pdf_filename.pdf"'

       return response
   
def generate_pdf_export(request, dealer_id):
       dealer = get_object_or_404(Dealer, id=dealer_id)
       products = ExportProduct.objects.filter(product__dealer_id=dealer_id)
       template = get_template('export/pdf_template.html')
       context = {'export_products': products,
                  'dealer': dealer}
       html_string = template.render(context)
       html = HTML(string=html_string)
       pdf_file = html.write_pdf()
       response = HttpResponse(pdf_file, content_type='application/pdf')
       response['Content-Disposition'] = 'filename="export_pdf_filename.pdf"'
       return response
   
def generate_pdf_employee_vacation(request, employee_id):
       employee = get_object_or_404(Employee, id=employee_id)
       vacations = Vacation.objects.filter(employee=employee)
       employee_totals = calculate_totals(employee_id)
       total_vacation =employee_totals.get('total_amount_vacation')
       template = get_template('vacation/pdf_template.html')
       context = {'vacations': vacations,
                  'employee': employee,
                  'total_vacation':total_vacation}
       html_string = template.render(context)
       html = HTML(string=html_string)
       pdf_file = html.write_pdf()
       response = HttpResponse(pdf_file, content_type='application/pdf')
       response['Content-Disposition'] = 'filename="vacation_pdf_filename.pdf"'
       return response
   

   
def generate_pdf_employee_withdraw(request, employee_id ):

       employee = get_object_or_404(Employee, id=employee_id)
       withdraws = EmployeeWithdraw.objects.filter(employee=employee)
       employee_totals = calculate_totals(employee_id)
       total_withdrawals = employee_totals['total_withdrawals']
       template = get_template('withdraw/pdf_template.html')
       context = {'withdraws': withdraws,
                  'employee': employee,
                  'total_withdrawals':total_withdrawals}
       html_string = template.render(context)
       html = HTML(string=html_string)
       pdf_file = html.write_pdf()
       response = HttpResponse(pdf_file, content_type='application/pdf')
       response['Content-Disposition'] = 'filename="employee_withdraw_pdf_filename.pdf"'
       return response
   

def generate_pdf_dealer_withdraw(request,  dealer_id):

       dealer = get_object_or_404(Dealer, id=dealer_id)
       withdraws = DealerWithdraw.objects.filter(dealer=dealer)
       dealer_totals = dealer_calculate_totals(dealer_id)
       total_withdrawals = dealer_totals['total_dealer_withdrawals']
       template = get_template('withdraw/pdf_template.html')
       context = {'withdraws': withdraws,
                  'dealer': dealer,
                  'total_withdrawals':total_withdrawals}
       html_string = template.render(context)
       html = HTML(string=html_string)
       pdf_file = html.write_pdf()
       response = HttpResponse(pdf_file, content_type='application/pdf')
       response['Content-Disposition'] = 'filename="dealer_withdraw_pdf_filename.pdf"'
       return response
   

