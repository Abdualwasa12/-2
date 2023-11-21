from django.db import models
from django.urls import reverse
from django.utils import timezone
from accounts.models import Profile

# Create your models here.
class Salary(models.Model):
    amount = models.IntegerField()
    date_from =models.DateField()
    date_to = models.DateField(blank=True,null=True)

    
    def calculate_total_salary(self):
        # Calculate the number of days between date_from and date_to
        days_difference = (self.date_to - self.date_from).days
        
        # Multiply the amount by the number of days
        total_salary = self.amount * days_difference
        
        return total_salary
    
    def __str__(self):
        return str(self.amount)


class Employee(models.Model):
    name =models.CharField(max_length=200)
    salary = models.OneToOneField(Salary,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='employees')



    class Meta:
        unique_together = ('name', 'salary')
        ordering = ['-salary']
    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse("employee:detail_employee",args=[self.id])
    
class OutEmployee(models.Model):
    employee = models.OneToOneField(Employee,on_delete=models.CASCADE)
    last_date = models.DateField(default=timezone.now)


    class Meta:
        ordering = ['-last_date']
        
    def __str__(self):
        return str(self.employee)
    
    def get_absolute_url(self):
        return reverse("employee:detail_employee",args=[self.employee.id])
    
    def save(self, *args, **kwargs):
    #  if the employee added to the OutEmployee model, it will Update the date_to field in the related Salary object to the last_date 
        self.employee.salary.date_to = self.last_date
        self.employee.salary.save()  # Save the related Salary object
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"{self.employee.name} - {self.last_date}"
