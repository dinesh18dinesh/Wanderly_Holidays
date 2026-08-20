from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES=[('male','Male'),('female','Female'),('other','Other')]
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone_country_code=models.CharField(max_length=8,blank=True,default='+91')
    phone_number=models.CharField(max_length=20,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,blank=True)
    address=models.TextField(blank=True)
    city=models.CharField(max_length=80,blank=True)
    state=models.CharField(max_length=80,blank=True)
    country=models.CharField(max_length=80,blank=True,default='India')
    pincode=models.CharField(max_length=15,blank=True)
    profile_picture=models.ImageField(upload_to='profiles/',blank=True,null=True)
    newsletter_subscribed=models.BooleanField(default=False)
    def __str__(self): return f"{self.user.username}'s profile"

@receiver(post_save,sender=User)
def create_or_update_profile(sender,instance,created,**kwargs):
    if created: Profile.objects.create(user=instance)
    else: Profile.objects.get_or_create(user=instance)
