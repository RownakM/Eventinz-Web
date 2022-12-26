from django.db import models

# Create your models here.

class user_login(models.Model):
    fname=models.CharField(max_length=200)
    lname=models.CharField(max_length=200)
    Email=models.EmailField()
    password=models.CharField(max_length=300)
    mobile_code=models.CharField(max_length=200)
    mobile=models.CharField(max_length=300)
    country=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    aboutme=models.TextField(blank=True)
    
    created_on=models.DateTimeField(auto_now_add=True)
    user_wallet=models.IntegerField(default=0)
    profile_image=models.ImageField(upload_to='user_profile_image/')
    class Meta:
        verbose_name_plural = "User Profile"