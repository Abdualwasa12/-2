from django.db import models
from django.urls import reverse
from accounts.models import Profile
from dealer.models import Dealer
# Create your models here.

class Material(models.Model):
    name = models.CharField(max_length=200)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)
    price = models.IntegerField()
    date = models.DateField()
    num_of_bill =models.PositiveIntegerField()
    description = models.TextField( blank=True,null=True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='materials')
    
    def __str__(self):
        return self.name
    