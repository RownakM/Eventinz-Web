from django.db import models

# from vendor_admin.models import vendor_categories

# Create your models here.



class event_categories(models.Model):
    category_name=models.CharField(max_length=400)
    category_img=models.ImageField(upload_to='ev_cats/images/')
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural = "Event Categories"

class event_sub_categories(models.Model):
    sub_category_name=models.CharField(max_length=400)
    category = models.ForeignKey(event_categories,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Event Sub Categories"
class event_categories_french(models.Model):
    category_name=models.CharField(max_length=400)
    class Meta:
        verbose_name_plural = "Event Categories (French)"
    def __str__(self):
        return self.category_name

class event_sub_categories_french(models.Model):
    sub_category_name=models.CharField(max_length=400)
    category = models.ForeignKey(event_categories_french,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Event Sub Categories (French)"

class Venue_Type(models.Model):
    venue_name=models.CharField(max_length=300)
    img=models.ImageField(upload_to='venue_img/imgs/')

    class Meta:
        verbose_name_plural = "Venue-Event Type"
    def __str__(self):
        return self.venue_name


class Venue_Details(models.Model):
    venue_name=models.ForeignKey(Venue_Type,on_delete=models.CASCADE)
    venue_subheading=models.CharField(max_length=300)
    venue_image=models.ImageField(upload_to='venue_content/image/detailed/')

    class Meta:
        verbose_name_plural='Venue Details'
  
class Venue_Type_by_venue(models.Model):
    venue_name=models.CharField(max_length=100)
    venue_image=models.ImageField(upload_to='venue_content/image/')

    class Meta:
        verbose_name_plural='Venue Type'
    def __str__(self):
        return self.venue_name

class Venue_main_home(models.Model):
    venue_head_image=models.ImageField(upload_to='venue_content/main_venue/image/')
    venue_header=models.CharField(max_length=300)
    venue_by_venue=models.CharField(max_length=300)
    venue_by_venue_subheading=models.CharField(max_length=300)


    venue_by_event=models.CharField(max_length=300)
    venue_by_event_subheading=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "'Venue' - Content Management"

class Exchange_Rates(models.Model):
    base_country=models.CharField(max_length=4000)
    dest_country=models.CharField(max_length=4000)
    ex_rate=models.CharField(max_length=5000)

class cron_activities(models.Model):
    cron_type=models.CharField(max_length=100)
    cron_purpose=models.CharField(max_length=200)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    status=models.CharField(max_length=300)


class Exchange_Rates_API(models.Model):
    email=models.CharField(max_length=400)
    password=models.CharField(max_length=500)
    apikey=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

class Our_Vendor_CMS(models.Model):
    background_image=models.ImageField(upload_to='our_vendor/bg_image/')
    Header_Text=models.CharField(max_length=3000)
    Display_text=models.CharField(max_length=4000)

    class Meta:
        verbose_name_plural = "'Our Vendor' - Page Header Management"












class Venue_Type_french(models.Model):
    venue_name=models.CharField(max_length=300)
    img=models.ImageField(upload_to='venue_img/imgs/')

    class Meta:
        verbose_name_plural = "Venue-Event Type"
    def __str__(self):
        return self.venue_name


class Venue_Details_french(models.Model):
    venue_name=models.ForeignKey(Venue_Type,on_delete=models.CASCADE)
    venue_subheading=models.CharField(max_length=300)
    venue_image=models.ImageField(upload_to='venue_content/image/detailed/')

    class Meta:
        verbose_name_plural='Venue Details'
  
class Venue_Type_by_venue_french(models.Model):
    venue_name=models.CharField(max_length=100)
    venue_image=models.ImageField(upload_to='venue_content/image/')

    class Meta:
        verbose_name_plural='Venue Type'
    def __str__(self):
        return self.venue_name

class Venue_main_home_french(models.Model):
    venue_head_image=models.ImageField(upload_to='venue_content/main_venue/image/')
    venue_header=models.CharField(max_length=300)
    venue_by_venue=models.CharField(max_length=300)
    venue_by_venue_subheading=models.CharField(max_length=300)


    venue_by_event=models.CharField(max_length=300)
    venue_by_event_subheading=models.CharField(max_length=300)

class Exchange_Rates_french(models.Model):
    base_country=models.CharField(max_length=4000)
    dest_country=models.CharField(max_length=4000)
    ex_rate=models.CharField(max_length=5000)

class cron_activities_french(models.Model):
    cron_type=models.CharField(max_length=100)
    cron_purpose=models.CharField(max_length=200)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    status=models.CharField(max_length=300)


class Exchange_Rates_API_french(models.Model):
    email=models.CharField(max_length=400)
    password=models.CharField(max_length=500)
    apikey=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

class Our_Vendor_CMS_french(models.Model):
    background_image=models.ImageField(upload_to='our_vendor/bg_image/')
    Header_Text=models.CharField(max_length=3000)
    Display_text=models.CharField(max_length=4000)