from django.contrib import admin
from .models import Salary, Employee,OutEmployee
# Register your models here.

admin.site.register(Salary)
admin.site.register(Employee)
admin.site.register(OutEmployee)

