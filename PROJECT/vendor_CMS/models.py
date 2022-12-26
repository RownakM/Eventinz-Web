from django.db import models

# Create your models here.

class vendor_header(models.Model):
    bg_image=models.ImageField(upload_to='vendor_site/images/hero/')
    Title=models.CharField(max_length=300)
    Sub_Title=models.CharField(max_length=200)
    Short_Text=models.CharField(max_length=200)
    class Meta:
        verbose_name_plural="Vendor Header"

class vendor_leads_CMS_main(models.Model):
    Heading=models.CharField(max_length=300)
    SubTitle=models.CharField(max_length=300)
    button_text=models.CharField(max_length=1000)
    class Meta:
        verbose_name_plural="Vendor Leads CMS"

class vendor_leads_Steps(models.Model):
    step_no=models.IntegerField()
    image=models.ImageField(upload_to='vendor_site/images/vendor_leads/icon/')
    Heading=models.CharField(max_length=300)
    Sub_Text=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural="Vendor Leads Steps"

class vendor_category_CMS(models.Model):
    Heading=models.CharField(max_length=300)
    Sub_Heading=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural="Vendor Category CMS"
class vendor_testimonials(models.Model):
    Heading=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural="Vendor Testimonials"

class our_clients_CMS(models.Model):
    Heading=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural="Vendor Clients CMS"

class our_clients(models.Model):
    image=models.ImageField(upload_to='vendor_site/images/our_clients/brand_images/')
    caption=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural="Vendor Clients"

class vendor_get_started(models.Model):
    Heading=models.CharField(max_length=300)
    Sub_Heading=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural="Vendor Get Started"
