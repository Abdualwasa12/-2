from django.db import models
from django.contrib.auth.models import User
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile' ,on_delete=models.CASCADE)
    image = models.ImageField( upload_to='profile_img', blank=True, null=True)
    address = models.CharField(max_length=100)
    join_date = models.DateTimeField(default = datetime.datetime.now)
    


    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")

    def __str__(self):
        return  '%s' %(self.user)

## create new user ---> create new empty profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
