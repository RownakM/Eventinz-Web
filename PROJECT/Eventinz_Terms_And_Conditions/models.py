from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class Eventinz_Terms(models.Model):
    page_image=models.ImageField(upload_to='tnc/content/')
    page_header=models.CharField(max_length=1000)
    content=HTMLField()
    class Meta:
        verbose_name_plural = 'Eventinz - Terms & Conditions'

class Eventinz_Privacy_Policy(models.Model):
    page_image=models.ImageField(upload_to='privacy/content/')
    page_header=models.CharField(max_length=1000)
    content=HTMLField()
    class Meta:
        verbose_name_plural = 'Eventinz - Privacy Policy'

class Eventinz_Terms_french(models.Model):
    page_image=models.ImageField(upload_to='tnc/content/')
    page_header=models.CharField(max_length=1000)
    content=HTMLField()

class Eventinz_Privacy_Policy_french(models.Model):
    page_image=models.ImageField(upload_to='privacy/content/')
    page_header=models.CharField(max_length=1000)
    content=HTMLField()