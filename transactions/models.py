from django.db import models
from dealer.models import Dealer
from employee.models import Employee
from accounts.models import Profile
# Create your models here.



class ImportProduct(models.Model):
    type_name= models.CharField(max_length=250 ,unique=False)
    yard = models.IntegerField(unique=False)
    
    class Meta:
        ordering = ['type_name']
    
    def __str__(self):
        return self.type_name

    def is_exported(self):
        # Check if there is a corresponding ExportProduct linked to this ImportProduct
        return "نعم" if hasattr(self, 'exportproduct') else "لا"

    
    
class ExportProduct(models.Model):
    type_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price_of_one = models.IntegerField()
    product = models.OneToOneField(ImportProduct, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.type_name
    
    def total_price(self):
        return self.quantity * self.price_of_one
    
############### Employee ##################

TYPE_OF_VACATION=(
    ( 'يوم' , "يوم"),
    ( 'نصف يوم' , "نصف يوم"),
    )

class Vacation(models.Model):
    type_vacation = models.CharField(max_length=200,choices=TYPE_OF_VACATION )
    date = models.DateField(blank=True,null=True)
    amount_vacation =models.FloatField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True)

    
    class Meta:
        ordering = ['-date']
    
    def __str__(self): 
        return str(self.type_vacation)
    
    def save(self, *args, **kwargs):
        if self.type_vacation == 'يوم':
            self.amount_vacation = 1
        elif self.type_vacation =='نصف يوم':
            self.amount_vacation = 0.5
            
        super(Vacation, self).save(*args, **kwargs)
    
class BaseWithdraw(models.Model):
    withdraw = models.IntegerField()
    date = models.DateField()
    description = models.TextField(blank=True,null=True)
    
    class Meta:
        abstract= True
        ordering = ['-date']
    
    def __str__(self):
        return str(self.withdraw)



class EmployeeWithdraw(BaseWithdraw):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, blank=True)

    
    
    
class DealerWithdraw(BaseWithdraw):
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE, blank=True)
