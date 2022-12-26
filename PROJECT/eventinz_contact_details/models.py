from django.db import models

# Create your models here.

class EV_Contact(models.Model):
    Company_Name=models.CharField(max_length = 1000)
    Address_Line_1=models.CharField(max_length = 2000)
    Address_Line_2=models.CharField(max_length = 2000,null=True,blank=True)
    City = models.CharField(max_length = 1000)
    State = models.CharField(max_length = 4000)
    Country = models.CharField(max_length = 2000)
    Phone_Number = models.CharField(max_length = 1000)
    Email = models.EmailField()
    facebook_url = models.URLField(null = True , blank = True)
    instagram_url=models.URLField(null = True , blank = True)
    twitter_url = models.URLField(null = True , blank = True)
    linkedin_url = models.URLField(null = True , blank = True)
    contact_page_image=models.ImageField(upload_to="contact_details/image/")
    class Meta:
        verbose_name_plural = "Eventinz - Contact Details"
