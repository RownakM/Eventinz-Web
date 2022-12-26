from email.policy import default
from django.db import models

from vendor_admin.models import Countries, Vendor_Users, vendor_categories
from user_dashboard.models import user_login

# Create your models here.
class event_budget_settings(models.Model):
    country=models.ForeignKey(Countries,on_delete=models.CASCADE)
    Minimum_Value=models.IntegerField()
    Maximum_Value=models.IntegerField(help_text = "Enter 2441139 For Above Minimum Value")
    class Meta:
        verbose_name_plural = "Event Budget Manager"
class event_entries(models.Model):
    Country=models.CharField(max_length=40)
    State=models.CharField(max_length=50)
    City=models.CharField(max_length=90)
    Event_Categories=models.CharField(max_length=100)
    Event_Sub_Categories=models.CharField(max_length=200)
    Heads=models.CharField(max_length=30)
    DOE=models.DateField()
    Budget=models.ForeignKey(event_budget_settings,on_delete=models.CASCADE)
    First_Name=models.CharField(max_length=200)
    Last_Name=models.CharField(max_length=200)
    Email=models.CharField(max_length=300)
    MCode=models.CharField(max_length=200)
    Mobile=models.CharField(max_length=200)
    Event_Desc=models.TextField()
    status=models.CharField(max_length=30,default='draft')
    user_type=models.CharField(max_length=30)
    package_type=models.CharField(max_length=100)
    vendor_type=models.CharField(max_length=400)
    created_on=models.DateTimeField(auto_now_add=True)
    ev_name=models.CharField(max_length=300)
    vendorjson=models.JSONField()
    is_archieve = models.BooleanField(default=False)
    unique_id = models.TextField(default = 0)

    class Meta:
        verbose_name_plural = "Event Entries"

class event_heads_manager(models.Model):
    Minimum_Value=models.IntegerField()
    Maximum_Value=models.IntegerField()

    class Meta:
        verbose_name_plural = "Event Guests Manager"

class event_planner_CMS(models.Model):
    title=models.CharField(max_length=400)
    image=models.ImageField(upload_to='event_planner_cms/images/')
    heading=models.CharField(max_length=400)
    sub_heading=models.CharField(max_length=400)
    class Meta:
        verbose_name_plural = "'Event Planner' - Manager"
class event_planner_CMS_french(models.Model):
    title=models.CharField(max_length=400)
    image=models.ImageField(upload_to='event_planner_cms/images/')
    heading=models.CharField(max_length=400)
    sub_heading=models.CharField(max_length=400)
    
class create_event_packages(models.Model):
    currency_country=models.ForeignKey(Countries,on_delete=models.CASCADE)
    premium_amount=models.IntegerField()
    freemium_features=models.TextField()
    premium_features=models.TextField()
    premium_validity = models.IntegerField(default=1,help_text='In Days')
    class Meta:
        verbose_name_plural = "'Create Event' - Packages"

class create_event_packages_french(models.Model):
    currency_country=models.ForeignKey(Countries,on_delete=models.CASCADE)
    premium_amount=models.IntegerField()
    freemium_features=models.TextField()
    premium_features=models.TextField()
    
class vendor_event_proposal(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    event_id=models.ForeignKey(event_entries,on_delete=models.CASCADE)
    cover_letter=models.TextField()

    total_amount=models.CharField(max_length=300)
    state_tax=models.CharField(max_length=4000,default='0')
    grand_total=models.CharField(max_length=4000,default='0')
    created_on=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=4000,default='NA')


class vendor_event_proposal_items(models.Model):
    proposal_id=models.ForeignKey(vendor_event_proposal,on_delete=models.CASCADE)
    item=models.TextField()
    rate=models.CharField(max_length=4000)
    qty=models.CharField(max_length=3000)
    unit=models.CharField(max_length=300)
    total=models.CharField(max_length=400)


class event_reviews_user_to_vendor(models.Model):
    event_id=models.ForeignKey(event_entries,on_delete=models.CASCADE)
    review_from=models.ForeignKey(user_login,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_date=models.DateTimeField(auto_now_add=True)
    review_star=models.IntegerField(default=0)
    vendor_id=models.ForeignKey(Vendor_Users,on_delete = models.CASCADE)

class event_reviews_vendor_to_user(models.Model):
    event_id=models.ForeignKey(event_entries,on_delete=models.CASCADE)
    review_from=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_date=models.DateTimeField(auto_now_add=True)
    review_star=models.IntegerField(default=0)