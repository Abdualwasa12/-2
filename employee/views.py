from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from dealer.models import Dealer
from transactions.models import EmployeeWithdraw,Vacation,DealerWithdraw,ExportProduct
from .models import Employee, Salary, OutEmployee
from django.contrib import messages
from .forms import EmployeeSalaryForm
import datetime
from django.db.models import Count,Sum
# Create your views here.

def employee(request):
    current_user = request.user.profile
    employees = Employee.objects.filter(user=current_user)


    # Get the list of employee IDs who are in the OutEmployee model
    out_employee_ids = OutEmployee.objects.filter(employee__user=current_user).values_list('employee', flat=True)

    # Update the date_to field for employees not in the OutEmployee model
    for employee in employees:
        if employee.id not in out_employee_ids:
            # Update the date_to field to the current date
            employee.salary.date_to = datetime.date.today()
            employee.salary.save()
        
        
    employees_not_in_outemployee = Employee.objects.filter(user=current_user).exclude(outemployee__isnull=False)
    employees_not_in_outemployee = Employee.objects.filter(user=current_user).annotate(out_employee_count=Count('outemployee')).filter(out_employee_count=0)


    return render(request, 'employee/list_employee.html', {'employees': employees,'employees_not_in_outemployee':employees_not_in_outemployee})




def add_edit_employee(request, employee_id=None):
    if employee_id is not None:
        employee = get_object_or_404(Employee, id=employee_id,user=request.user.profile)
        salary = employee.salary  # Get the associated Salary instance
    else:
        employee = None
        salary = None

    if request.method == 'POST':
        form = EmployeeSalaryForm(request.POST, instance=employee)
        if form.is_valid():
            # Create or update Salary instance
            if salary is None:
                salary = Salary(
                    amount=form.cleaned_data['amount'],
                    date_from=form.cleaned_data['date_from'],
                )
                salary.save()
            else:
                salary.amount = form.cleaned_data['amount']
                salary.date_from = form.cleaned_data['date_from']
                salary.save()

            # Save the Employee instance
            employee = form.save(commit=False)
            employee.salary = salary
            employee.user = request.user.profile
            employee.save()

            messages.success(request, 'تم تسجيل العميل بنجاح')
            return redirect('employee:list_employee')
    else:
        initial_data = {'date_from': None, 'amount': None}  # Default values when adding a new employee
        if salary is not None:
            initial_data['date_from'] = salary.date_from
            initial_data['amount'] = salary.amount
        form = EmployeeSalaryForm(instance=employee, initial=initial_data)
    return render(request, 'employee/add_edit_employee.html', {'form': form, 'employee': employee})

def delete_employee(request, id ):
    employee =get_object_or_404(Employee, id=id)
    if employee.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this hoooo")
    if request.method == 'POST':
        employee.delete()

        messages.success(request,'تم حذف العميل بنجاح')
        return redirect('employee:list_employee')
    return render(request,'employee/delete_employee.html')


def detail_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if employee.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this hoooo")
    employee_totals = calculate_totals(employee_id)
    total_withdrawals = employee_totals['total_withdrawals']
    adjusted_total_salary = employee_totals['adjusted_total_salary']
    total_amount_vacation = employee_totals['total_amount_vacation']
    salary_vacation =employee_totals['salary_vacation']

    return render(request,'employee/detail_employee.html', {'employee': employee,
                                                            'adjusted_total_salary': adjusted_total_salary,
                                                            'total_withdrawals':total_withdrawals,
                                                            'salary_vacation':salary_vacation,
                                                            'total_amount_vacation':total_amount_vacation})





################### OutEmployee #####################


def out_employee(request):
    current_user = request.user.profile
    out_employees = OutEmployee.objects.filter(employee__user=current_user)
    return render(request, 'out_employee/list_outemployee.html',{'out_employees':out_employees})

def add_employee_to_out(request, employee_id):   
    employee = get_object_or_404(Employee, id =employee_id)
    if employee.user != request.user.profile:
        return HttpResponseForbidden("You are not authorized to delete this hoooo")
    if request.method == 'POST':
        OutEmployee.objects.create(employee=employee)
        messages.success(request,' تم إخارج العامل بنجاح')
        return redirect('employee:list_out_employee')
    return render(request, 'out_employee/add_to_out.html')




########## calculate totals ########### reusable func

def calculate_totals(id):
    ######### Employee ##########
    employee = get_object_or_404(Employee, id=id)
    
        # Calculate the total amount_vacation for the employee
    total_amount_vacation=Vacation.objects.filter(employee=employee).aggregate(Sum('amount_vacation'))['amount_vacation__sum']
    # the vacation discount
    # Initialize salary_vacation with a default value (e.g., 0)
    salary_vacation = 0
    # Check if total_amount_vacation is not None
    if total_amount_vacation is None:
        total_amount_vacation=0
    else:
        salary_vacation =total_amount_vacation * employee.salary.amount   
     
     # Check if dealer_totals is None, indicating no records found

    # Calculate the total salary as before
    total_salary =Salary.calculate_total_salary(employee.salary)
    # Calculate the sum of withdrawals for this employee
    withdrawals = EmployeeWithdraw.objects.filter(employee=employee)
    total_withdrawals = sum(withdraw.withdraw for withdraw in withdrawals)
    # Subtract total withdrawals from total salary
    adjusted_total_salary = total_salary - total_withdrawals - salary_vacation

    return {
        'adjusted_total_salary': adjusted_total_salary,
        'total_withdrawals':total_withdrawals,
        'total_amount_vacation': total_amount_vacation,
        'salary_vacation': salary_vacation,

    }