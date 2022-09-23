from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import URLValidator

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    streak=models.IntegerField()
    edStat=models.CharField(max_length=120,blank=True)
    abt=models.TextField(max_length=500,blank=True)
    birthDate=models.DateField(null=True,blank=True)
    city=models.CharField(max_length=50,blank=True)
    country=models.CharField(max_length=50,blank=True)
    career=models.CharField(max_length=120,blank=True)
    interests=models.JSONField(null=True,default=list)
    communities=models.JSONField(null=True,default=list)
    pp=models.ImageField()

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()