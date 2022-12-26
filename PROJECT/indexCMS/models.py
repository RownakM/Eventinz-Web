from distutils.command import upload
from django.db import models

# Create your models here.
class index_slider(models.Model):
    image=models.ImageField(upload_to='main_site/slider/img')
    class Meta:
        verbose_name_plural = "Index Slider"

class index_headers(models.Model):
    Header=models.CharField(max_length=300)
    sub_header=models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Index Headers"

class how_eventinz_works(models.Model):
    Header_Text=models.CharField(max_length=200)
    Sub_Text=models.CharField(max_length=200)
    background_image=models.ImageField(upload_to='main_site/how_eventinz_works/bg_image')
    Step_1_Icon=models.ImageField(upload_to='main_site/how_eventinz_works/icons')
    Step_1_Text=models.CharField(max_length=30)
    Step_2_Icon=models.ImageField(upload_to='main_site/how_eventinz_works/icons')
    Step_2_Text=models.CharField(max_length=40)
    Step_3_Icon=models.ImageField(upload_to='main_site/how_eventinz_works/icons')
    Step_3_Text=models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = "How Eventinz Works"

class advertisement(models.Model):
    adv_heading=models.CharField(max_length=400)
    adv_subtext=models.CharField(max_length=400)
    adv_bg_image=models.ImageField(upload_to='main_site/advertisement/bg')
    adv_image=models.ImageField(upload_to='main_site/advertisement/img')
    class Meta:
        verbose_name_plural = "Advertisements"
    

class Vendor_Deals_Index_CMS(models.Model):
    heading=models.CharField(max_length=400)
    sub_heading=models.CharField(max_length=400)
    Package_Button_Text=models.CharField(max_length=300)
    Deals_Button_Text=models.CharField(max_length=400)

    class Meta:
        verbose_name_plural = 'Vendor Deals - Index CMS'

class Vendor_Categories_Text(models.Model):
    Heading=models.CharField(max_length=400)
    Sub_Heading=models.CharField(max_length=400)

    class Meta:
        verbose_name_plural = 'Vendor Categories - Index'



class Packages_CMS(models.Model):
    Heading = models.CharField(max_length=1000)
    image=models.ImageField(upload_to="main_site/package_cms/img")













class index_slider_french(models.Model):
    image=models.ImageField(upload_to='main_site/slider/img')
    class Meta:
        verbose_name_plural = "Index Slider"

class index_headers_french(models.Model):
    Header=models.CharField(max_length=300)
    sub_header=models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "Index Headers"

class how_eventinz_works_french(models.Model):
    Header_Text=models.CharField(max_length=200)
    Sub_Text=models.CharField(max_length=200)
    background_image=models.ImageField(upload_to='main_site/how_eventinz_works/bg_image')
    Step_1_Icon=models.ImageField(upload_to='main_site/how_eventinz_works/icons')
    Step_1_Text=models.CharField(max_length=30)
    Step_2_Icon=models.ImageField(upload_to='main_site/how_eventinz_works/icons')
    Step_2_Text=models.CharField(max_length=40)
    Step_3_Icon=models.ImageField(upload_to='main_site/how_eventinz_works/icons')
    Step_3_Text=models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = "How Eventinz Works"

class advertisement_french(models.Model):
    adv_heading=models.CharField(max_length=400)
    adv_subtext=models.CharField(max_length=400)
    adv_bg_image=models.ImageField(upload_to='main_site/advertisement/bg')
    adv_image=models.ImageField(upload_to='main_site/advertisement/img')
    class Meta:
        verbose_name_plural = "Advertisements"
    

class Vendor_Deals_Index_CMS_french(models.Model):
    heading=models.CharField(max_length=400)
    sub_heading=models.CharField(max_length=400)
    Package_Button_Text=models.CharField(max_length=300)
    Deals_Button_Text=models.CharField(max_length=400)

class Vendor_Categories_Text_french(models.Model):
    Heading=models.CharField(max_length=400)
    Sub_Heading=models.CharField(max_length=400)