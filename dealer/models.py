from django.db import models
from django.urls import reverse
from accounts.models import Profile

# Create your models here.

class Dealer(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='dealers')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("dealer:detail_dealer",args=[self.id])
    
    