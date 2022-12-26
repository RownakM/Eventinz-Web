from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class Header(models.Model):
    image=models.ImageField(upload_to='header_image')
    Heading=models.CharField(max_length=300)
    button_text=models.CharField(max_length=300)
    

class Entries(models.Model):
    fname=models.CharField(max_length=300)
    lname=models.CharField(max_length=300)

    email=models.EmailField()
    mobile=models.CharField(max_length=100)
    User_Type=models.CharField(max_length=200,choices=[
        ('Vendor','Vendor'),
        ('User','User')
    ])
    created_on=models.DateTimeField(auto_now_add=True)
    country=models.CharField(max_length=200)
class About(models.Model):
    Heading=models.CharField(max_length=200)
    About_text=HTMLField()

class Mail_User(models.Model):
    content=HTMLField()
    created_on=models.DateTimeField(auto_now_add=True)
    subject=models.CharField(max_length=300)
class Mail_Vendor(models.Model):
    content=HTMLField()
    created_on=models.DateTimeField(auto_now_add=True)
    subject=models.CharField(max_length=300)


CHOICES=(
    ('0','Subscribed'),
    ('1','Un-Subscribed')
)
class NewsLetter(models.Model):
    email=models.EmailField()
    created_on=models.DateTimeField(auto_now_add=True)
    subscribe_status=models.CharField(max_length=30,choices=CHOICES,default='0')

send_to_list=(
    ('Vendors','Vendors'),
    ('Vendors - Registered Group','Vendors - Registered Group'),
    ('Hosts' , 'Hosts'),
    ('Hosts - Registered Group','Hosts - Registered Group'),
    ('Newsletters','Newsletter Subscribers')
)
class Schedule_Mails(models.Model):

    Send_to=models.CharField(max_length=4000,choices=send_to_list)
    subject=models.TextField()
    # content=HTMLField()
    scheduled_time=models.DateTimeField()
