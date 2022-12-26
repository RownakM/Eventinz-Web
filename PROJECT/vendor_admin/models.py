from email.policy import default
from django.db import models
import uuid

# from time import timezone
from content_app.models import event_categories,event_categories_french
from user_dashboard.models import user_login
from tinymce.models import HTMLField
# import models.JSONField
# from django.contrib.postgres.fields import models.JSONField
# from django.db.models import models.JSONField


# Create your models here.

class Vendor_Users(models.Model):
    Profile_Img=models.ImageField(upload_to='vendors/profile/images',blank=True,null=True)
    First_Name=models.CharField(max_length=200)
    Last_Name=models.CharField(max_length=200)
    Email=models.EmailField()
    Password=models.CharField(max_length=300)
    User_ID=models.CharField(max_length=100)
    phone_code=models.CharField(max_length=100,default=0)
    Mobile=models.CharField(blank=True,null=True,max_length=5000)
    Alternative_Mobile=models.CharField(blank=True,null=True,max_length=5000)
    is_otp_verified=models.BooleanField(default=False)
    Company_Name=models.CharField(max_length=200)
    Company_Address=models.TextField(blank=True,null=True)
    Company_description=models.TextField(blank=True,null=True)
    Company_url=models.URLField(blank=True,null=True)
    country_code=models.CharField(max_length=300)
    state_code=models.CharField(max_length=200)
    country_name=models.CharField(max_length=200)
    state_name=models.CharField(max_length=100)
    city_name = models.CharField(max_length = 100 , default = 'None')
    created_on=models.DateTimeField(auto_now_add=True)
    package=models.CharField(blank=True,null=True,max_length=200)
    price=models.IntegerField(blank=True,null=True)
    valid_till=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    facebook_url=models.CharField(max_length=400,null=True,blank=True)
    instagram_url=models.CharField(max_length=400,null=True,blank=True)
    twitter_url=models.CharField(max_length=400,null=True,blank=True)
    linkedin_url=models.CharField(max_length=400,null=True,blank=True)
    max_budget=models.IntegerField(default=0)
    min_budget=models.IntegerField(default=0)
    event_category_serve=models.JSONField(default=dict)
    question_field=models.JSONField(default=dict)
    caterer_field=models.JSONField(default=dict)
    vendor_wallet=models.IntegerField(default=0)
    event_categories=models.ForeignKey(event_categories,on_delete=models.CASCADE,blank=True,default=3)
    event_subcat=models.CharField(max_length=400,default='none')
    vendor_categories=models.JSONField(default=dict)
    profile_clicks=models.IntegerField(default=0)
    vendor_sub_cat_data=models.TextField(default='all')

    profile_complete = models.BooleanField(default=False)
    def __str__(self):
        return self.Company_Name
    class Meta:
        verbose_name_plural = "Vendor Profile"

class vendor_packages(models.Model):
    is_enterprise_vendor=models.BooleanField()
    package_name=models.CharField(max_length=200)
    package_features=models.CharField(max_length=300)
    price=models.IntegerField(default=0)
    price_quarter=models.IntegerField(default=0)
    price_biannual=models.IntegerField(default=0)
    price_monthly = models.IntegerField(default=0)
    package_description=models.TextField()
    lead_count=models.IntegerField(default=10)
    class Meta:
        verbose_name_plural = "Vendor Packages"

class vendor_subscription(models.Model):
    
    package_name=models.CharField(max_length=300,default='NAa',blank=True)
    package_description=models.CharField(max_length=200,default='NAa',blank=True)
    package_fee=models.BigIntegerField(default=123,blank=True)
    service_fee=models.FloatField(default=12,blank=True)
    service_currency=models.CharField(max_length=300,default='USD')
    payment_by=models.CharField(max_length=300,default='NAa',blank=True)
    time=models.CharField(max_length=300,default='NAa',blank=True)
    valid_from=models.DateTimeField(blank=True)
    valid_to=models.DateTimeField(blank=True)
    invoice_date=models.DateTimeField(auto_now_add=True)
    invoice_id=models.CharField(max_length=400,default='NAa',blank=True)
    Vendor_name=models.CharField(max_length=200,default='NAa',blank=True)
    Vendor_company_name=models.CharField(max_length=300,default='NAa',blank=True)
    vendor_phone=models.BigIntegerField(default=123,blank=True)
    vendor_email=models.EmailField(default='NAa',blank=True)
    purchase_type=models.CharField(max_length=300,default='NAa',blank=True)
    status=models.CharField(max_length=200)
    country_cuurency=models.CharField(max_length=30)
    vendor_categories=models.CharField(max_length=400)
    
    class Meta:
        verbose_name_plural = "Vendor Subscription"

class currency_model(models.Model):
    currency_name=models.CharField(max_length=200)
    currency_code=models.CharField(max_length=20)
    country=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = "Currency"
    

class Countries(models.Model):
    name=models.CharField(max_length=300)
    phone_code=models.CharField(max_length=30)
    capital=models.CharField(max_length=300)
    currency=models.CharField(max_length=200)
    latitude=models.CharField(max_length=300)
    longitude=models.CharField(max_length=300)
    region=models.CharField(max_length=300)
    class Meta:
        verbose_name_plural = "Countries"
    def __str__(self):
        return self.name

class States(models.Model):
    name=models.CharField(max_length=300)
    country_id=models.CharField(max_length=200)
    country_code=models.CharField(max_length=200)
    country_name=models.CharField(max_length=300)
    state_code=models.CharField(max_length=300)
    latitude=models.CharField(max_length=300,blank=True,default='NA')
    longitude=models.CharField(max_length=300,blank=True,default='NA')
    class Meta:
        verbose_name_plural = "States"

class Cities(models.Model):
    name=models.CharField(max_length=300)
    state_id=models.CharField(max_length=300)
    state_code=models.CharField(max_length=300)
    state_name=models.CharField(max_length=300)
    country_id=models.CharField(max_length=300)
    country_code=models.CharField(max_length=300)
    country_name=models.CharField(max_length=300)
    latitude=models.CharField(max_length=300,default='NA')
    longitude=models.CharField(max_length=300,default='NA')
    class Meta:
        verbose_name_plural = "Cities"

class total_sales(models.Model):
    vendor_id=models.CharField(max_length=30)
    Jan_sales=models.IntegerField(default=0,blank=True)
    Feb_sales=models.IntegerField(default=0,blank=True)
    Mar_sales=models.IntegerField(default=0,blank=True)
    Apr_sales=models.IntegerField(default=0,blank=True)
    May_sales=models.IntegerField(default=0,blank=True)
    Jun_sales=models.IntegerField(default=0,blank=True)
    Jul_sales=models.IntegerField(default=0,blank=True)
    Aug_sales=models.IntegerField(default=0,blank=True)
    Sep_sales=models.IntegerField(default=0,blank=True)
    Oct_sales=models.IntegerField(default=0,blank=True)
    Nov_sales=models.IntegerField(default=0,blank=True)
    Dec_sales=models.IntegerField(default=0,blank=True)
    class Meta:
        verbose_name_plural = "Total Sales"

class total_earnings(models.Model):
    vendor_id=models.CharField(max_length=30)
    Jan_earnings=models.IntegerField(default=0)
    Feb_earnings=models.IntegerField(default=0)
    Mar_earnings=models.IntegerField(default=0)
    Apr_earnings=models.IntegerField(default=0)
    May_earnings=models.IntegerField(default=0)
    Jun_earnings=models.IntegerField(default=0)
    Jul_earnings=models.IntegerField(default=0)
    Aug_earnings=models.IntegerField(default=0)
    Sep_earnings=models.IntegerField(default=0)
    Oct_earnings=models.IntegerField(default=0)
    Nov_earnings=models.IntegerField(default=0)
    Dec_earnings=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Total Earnings"
class total_orders(models.Model):
    vendor_id=models.CharField(max_length=30)
    order_count=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Total Orders"
class total_accepted_orders(models.Model):
    vendor_id=models.CharField(max_length=300)
    order_count=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Total Accepted Orders"
class total_rejected_orders(models.Model):
    vendor_id=models.CharField(max_length=300)
    order_count=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Total Rejected Orders"

class total_sales_count(models.Model):
    vendor_id=models.CharField(max_length=30)
    total_count=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Total Sales Count"
class total_earnings_count(models.Model):
    vendor_id=models.CharField(max_length=30)
    total_count=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Total Earnings Count"
class vendor_categories(models.Model):
    category_icon=models.ImageField(upload_to='vendors/icons/categories')
    category_name=models.CharField(max_length=400)
    category_cover_image=models.ImageField(upload_to='vendors/bg/categories')
    thumbnail_cover_image=models.ImageField(upload_to='vendors/thumbnail/categories')
    class Meta:
        verbose_name_plural = "Vendor Categories"
    def __str__(self):
        return self.category_name
class vendor_categories_french(models.Model):
    category_icon=models.ImageField(upload_to='vendors/icons/categories_french')
    category_name=models.CharField(max_length=400)
    category_cover_image=models.ImageField(upload_to='vendors/bg/categories_french')
    class Meta:
        verbose_name_plural = "Vendor Categories (French)"
    def __str__(self):
        return self.category_name

class vendor_sub_categories(models.Model):
    sub_category_name=models.CharField(max_length=200)
    # CHOICELIST=vendor_categories.objects.all()
    main_category=models.ForeignKey(vendor_categories,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Vendor Sub Categories"

class vendor_sub_categories_french(models.Model):
    sub_category_name=models.CharField(max_length=200)
    # CHOICELIST=vendor_categories.objects.all()
    main_category=models.ForeignKey(vendor_categories_french,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Vendor Sub Categories (French)"

class ChoiceList(models.Model):
    choice=models.CharField(max_length=15)
    def __str__(self):
        return self.choice
class SampleModel(models.Model):
    CHOICELIST=ChoiceList.objects.all()
    name=models.CharField(max_length=15)
    your_choice=models.ForeignKey(ChoiceList,on_delete=models.CASCADE)

from datetime import datetime

class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=10000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000000)

class Listings_Data(models.Model):
    Listing_type=models.ForeignKey(event_categories,on_delete=models.CASCADE)
    Listing_name=models.CharField(max_length=300)
    Max_Budget=models.IntegerField()
    Min_Budget=models.IntegerField()
    Description=HTMLField()
    feature_sets=models.JSONField()
    caterer_sets=models.JSONField()
    capacity_info=models.JSONField()
    atmosphere_sets=models.JSONField()
    speciality_sets=models.JSONField()
    event_planner_sets=models.JSONField()
    photo_vdo_sets=models.JSONField()
    DnR=models.JSONField()
    vendor_id=models.CharField(max_length=300)


class vendor_question_type(models.Model):
    question_type=models.CharField(max_length=300)
    def __str__(self):
        return self.question_type

class vendor_questions(models.Model):
    Question_Category=models.ForeignKey(vendor_categories,on_delete=models.CASCADE)
    # Question_Type=models.ForeignKey(vendor_question_type,on_delete=models.CASCADE)
    Question_Icon=models.ImageField(upload_to='main_site/vendor/question_category/images/')
    Question_Text=models.CharField(max_length=300,help_text='Keep it short and simple')
    Question_display_text=models.CharField(max_length=300,default=0)
    def __str__(self):
        return self.Question_Text
    class Meta:
        verbose_name_plural = "Vendor Features"

class vendor_public_packages(models.Model):
    package_name=models.CharField(max_length=200)
    what_included=HTMLField()
    package_price=models.IntegerField()
    package_price_range_max=models.IntegerField()
    package_price_range_min=models.IntegerField()
    package_category=models.CharField(max_length=300)
    category_name=models.CharField(max_length=300)
    package_for=models.CharField(max_length=300)
    valid_till=models.DateField()
    created_on=models.DateTimeField(auto_now_add=True)
    vendor_id=models.CharField(max_length=300)
    vendor_name=models.CharField(max_length=400)
    location_country_code=models.CharField(max_length=400,default='24',blank=True)
    location_state_code=models.CharField(max_length=400,default='0',blank=True)
    attendee_range=models.CharField(max_length=400,default='0')
    pricing_model=models.CharField(max_length=400,default='0')
    image=models.ImageField(upload_to="vendor_public_packages/images/",default=0)
    class Meta:
        verbose_name_plural = "Vendor Hosted Packages" 
    # vendor_address=models.CharField(max)
class vendor_public_deals(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    package_name=models.ForeignKey(vendor_public_packages,on_delete=models.CASCADE)
    deal_name=models.CharField(max_length=300)
    deal_price=models.CharField(max_length=4000)
    deal_by=models.CharField(max_length=4000)
    created_on=models.DateTimeField(auto_now_add=True)

import uuid
class vendor_gallery(models.Model):
    photo_src=models.ImageField(upload_to='main_site/vendor_photos/uploads/')
    photo_category=models.CharField(max_length=200)
    category_name=models.CharField(max_length=300)
    photo_id=models.CharField(default=uuid.uuid4(),max_length=300)
    vendor_email=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "Vendor Gallery"


class vendor_quote_invoice(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    quote_id=models.CharField(max_length=300)
    link_id=models.CharField(max_length=300)
    quotation_items=models.JSONField(default=dict)
    created_on=models.DateTimeField(auto_now_add=True)
    payment_terms=models.TextField()
    milestone=models.FloatField(max_length=300,default=0)
    milestone_type=models.CharField(max_length=300,default='amt')
    total_amt=models.CharField(max_length=300,default='0')
    valid_till=models.DateField()
    quote_user=models.ForeignKey(user_login,on_delete=models.CASCADE)
    short_link=models.CharField(max_length=400,default='0')
    tax_percent=models.FloatField(default=0)
    # quote_user=models.ForeignKey(user_login,on_delete=models.CASCADE,blank=True)


class request_a_quote(models.Model):
    fname=models.CharField(max_length=400)
    lname=models.CharField(max_length=400)
    email=models.EmailField()
    phone=models.CharField(max_length=300)
    event_type=models.CharField(max_length=400)
    appx_date=models.DateField()
    no_of_guests=models.CharField(max_length=300)
    msg=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    quote_id=models.ForeignKey(vendor_quote_invoice,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=200,default='pending')
    v_link=models.CharField(max_length=200,default='no')
    pay_num = models.CharField(max_length = 200 , default = '1')
    class Meta: 
        verbose_name_plural = "Request A Quote - Entries"

class search_cms(models.Model):
    category_name=models.ForeignKey(vendor_categories,on_delete=models.CASCADE)
    search_subheading=models.CharField(max_length=300)
    search_image=models.ImageField(upload_to='search_content/image/detailed/')
    class Meta: 
        verbose_name_plural = "Search CMS"


class Vendor_bank_listing(models.Model):
    Vendor_Id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    Bank_Name=models.CharField(max_length=1000)
    Account_Name=models.CharField(max_length=1000)
    Bank_Account_Number=models.CharField(max_length=4000)
    Country=models.CharField(max_length=1000)
    Code_Banque=models.CharField(max_length=2000)
    Code_Guichet=models.CharField(max_length=3000)
    Cle_RIB=models.CharField(max_length=3000)
    IBAN=models.CharField(max_length=5000)
    Code_Swift=models.CharField(max_length=4000)
    Domiciliation = models.CharField(max_length=3000)
    PayPal_Account_Name=models.CharField(max_length=3000)
    Paypal_ID=models.CharField(max_length=4000)
    MoMo_Number=models.CharField(max_length=5000)
    is_bank=models.BooleanField(default=False)
    is_paypal = models.BooleanField(default=False)
    is_momo = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Vendor Bank Details"

class vendor_filter_answers(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    question_id=models.ForeignKey(vendor_questions,on_delete=models.CASCADE)
    answer_type=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    
leads_CHOICES={
    ('Year','Year'),
    ('Month','Month'),
    ('Quarter','Quarter'),
    ('Half-Yearly','Half-Yearly')
}

class vendor_leads_package(models.Model):
    package_image = models.ImageField(upload_to='leads_package/vendor/files/')
    package_name = models.CharField(max_length=5000)
    package_desc = models.TextField()
    package_fee = models.CharField(max_length=5000,help_text="In FCFA")
    lead_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_type = models.CharField(max_length=4000,choices = leads_CHOICES)

    class Meta: 
        verbose_name_plural = "Vendor Leads - Package"
faq_choices={
    ('active','active'),
    ('deactive','deactive')
}

class Vendor_FAQ(models.Model):
    Question = models.TextField()
    Answer = HTMLField()
    status = models.CharField(default = 'deactive',max_length = 1000,choices = faq_choices)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = "Vendor FAQ Page"