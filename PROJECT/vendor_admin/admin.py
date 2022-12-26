import datetime
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin
from admin_totals.admin import ModelAdminTotals
from django.db.models.functions import Coalesce
from django.db.models import Sum, Avg
from currency_symbols import CurrencySymbols
from vendor_wallet.models import vendor_wallet_manager
from numerize import numerize
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter, NumericRangeFilter
import pycountry



from django.contrib import admin
from vendor_admin import models
from import_export import resources

from django.utils.safestring import mark_safe

# Register your models here.
class Vendor_list(admin.ModelAdmin):
    list_display=['First_Name','Last_Name','Email','Mobile','Alternative_Mobile','is_otp_verified','profile_complete','Profile_Click','Company_Name','Company_Address','Company_url','package','Price','Enrolled_Categories','Payment_Method','Hosted_Packages','Created_On','Created_Time','Bank_Details','Leads','Last_Recharged']
    list_per_page=20

    search_fields=['Email','First_Name','Last_Name','Company_Name']
    list_filter=['package']
   
    def Price(self,obj):
        try:

            base_country = models.vendor_subscription.objects.get(vendor_email=obj.Email).country_cuurency
            # country_code = pycountry.countries.get(name=base_country).alpha_2
            price = obj.price
            dest_country = 'CAD'
            currency_icon = str(CurrencySymbols.get_symbol(dest_country))
            import requests

            url = 'https://api.exchangerate.host/convert?from='+base_country+'&to=CAD'
            response = requests.get(url)
            data = response.json()
            onefcfa=float(data['info']['rate'])
            
            total=round(onefcfa*float(price),2)
            return ('CAD '+str(total))
        except models.vendor_subscription.DoesNotExist:
            return '-'
        except TypeError:
            return 'TypeError'
        except models.vendor_subscription.MultipleObjectsReturned:
            return 'Multiple Objects Detected'

    def Created_On(self,obj):
        return obj.created_on.date()
    
    def Created_Time(self,obj):
        return obj.created_on.strftime("%H:%M:%S")
    def Hosted_Packages(self,obj):
        db = models.vendor_public_packages.objects.filter(vendor_id=obj.Email).distinct('package_name')
        return db.count()
    
    def Bank_Details(self,obj):
        try:
            db = models.Vendor_bank_listing.objects.get(Vendor_Id=obj.id)
            url = reverse('admin:%s_%s_change' % (db._meta.app_label,  db._meta.model_name),  args=[db.id] )
            return mark_safe('<a href="%s">View</a>' % (url))

        except models.Vendor_bank_listing.DoesNotExist:
            return 'Bank Details Not Added'
    def Profile_Click(self,obj):
        click = obj.profile_clicks
        if 0 <= click < 100:
            return mark_safe('<font color="red"><b>'+str(click)+'</b></font>')
        if 100 <= click < 300:
            return mark_safe('<font color="blue"><b>'+str(click)+'</b></font>')
        if 300 <= click < 1000:
            return mark_safe('<font color="violet"><b>'+str(click)+'</b></font>')
        else:
            return mark_safe('<font color="green"><b>'+str(click)+'</b></font>')


    def Enrolled_Categories(self,obj):
        try:
            db = models.vendor_subscription.objects.get(vendor_email = obj.Email)
            category_string=db.vendor_categories
            category_string_list=category_string.split('__#__')
            category_defined=[]
            for i in category_string_list:
                if i == '':
                    break
                category_name=models.vendor_categories.objects.get(id=i).category_name
                category_defined.append(category_name)
            separator=' , '
            text=separator.join(category_defined)
            return text
        except models.vendor_subscription.MultipleObjectsReturned:
            return 'Multiple Objects Returned'
    
    def Payment_Method(self,obj):
        try:

            db = models.Vendor_bank_listing.objects.get(Vendor_Id=obj.id)
        except models.Vendor_bank_listing.DoesNotExist:
            db = None
        method = []
        if db is None:
            return 'Payment Method Not Added'
        else:

            if db.is_bank:
                method.append('Bank')
            if db.is_momo:
                method.append('MoMo')
            if db.is_paypal:
                method.append('Paypal')
            separator = ','
            text = separator.join(method)
            return text

    def Leads(self,obj):
        try:
            db = vendor_wallet_manager.objects.get(vendor_id=obj.id)
            return (str(db.remaining_balance)+' / '+str(db.total_balance))
        except vendor_wallet_manager.MultipleObjectsReturned:
            return 'Multiple Objects Returned'
        
    def Last_Recharged(self,obj):
        try:
            db = vendor_wallet_manager.objects.get(vendor_id=obj.id)
            return (db.last_recharged_on)
        except vendor_wallet_manager.MultipleObjectsReturned:
            return 'Multiple Objects Returned'

admin.site.register(models.Vendor_Users,Vendor_list)

class vendor_subscription_custom(ImportExportModelAdmin,admin.ModelAdmin):
    readonly_fields = ('Vendor_name','Payment_By','Package_Fee','Service_Fee','Service_Currency','Enrolled_Categories')
    # fields = ('package_name', 'package_fee', 'get_c')
    list_display=['Vendor_Name','Vendor_company_name','vendor_phone','purchase_type','package_name','Package_Fee','Payment_By','Service_Fee','Service_Currency','Enrolled_Categories','vendor_email']
    search_fields=['Payment_By']
    list_filter=['payment_by']
    list_totals = [('package_fee', Sum)]
    list_per_page=5
    def Vendor_Name(self,obj):
        return obj.Vendor_name
    def Payment_By(self, obj):
        if obj.payment_by == 'momo':
            return 'MTN MoMo Pay'
        else:
            return 'Paypal'
    def Package_Fee(self, obj):
        currency = str(CurrencySymbols.get_symbol(obj.country_cuurency))
        pack=numerize.numerize(obj.package_fee)
        try:
            return (currency+" {:.2f}".format(float(pack)))
        except ValueError:
            return (currency+" "+pack)

        
    def Service_Fee(self,obj):
        
        return ("{:.2f}".format(float(obj.service_fee)))
    def Service_Currency(self,obj):
        if obj.payment_by == 'momo':
            return ("No Data Available")
        if obj.payment_by == 'paypal':

            return obj.service_currency
    # def Package_Currency(self, obj):
    #     if obj.country_cuurency == 'XOF':
    #         return 'F CFA'
    #     else:
    #         return obj.country_cuurency
    
    def Enrolled_Categories(self,obj):
        category_string=obj.vendor_categories
        category_string_list=category_string.split('__#__')
        category_defined=[]
        for i in category_string_list:
            if i == '':
                break
            category_name=models.vendor_categories.objects.get(id=i).category_name
            category_defined.append(category_name)
        separator=' , '
        text=separator.join(category_defined)
        return text
        

admin.site.register(models.vendor_subscription,vendor_subscription_custom)
class Vendor_Packages(admin.ModelAdmin):
    list_display = ['package_name','price','price_quarter','price_biannual','Package_Features','is_enterprise_vendor']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request , obj=None):
        return False
    def Package_Features(self,request,obj=None):
        return mark_safe(obj.package_description)
admin.site.register(models.vendor_packages)
admin.site.register(models.currency_model)
class countriesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=['id','name','phone_code','capital','currency','latitude','longitude','region']
    list_per_page=20
    list_filter=['region']
    search_fields=['name','phone_code','capital','currency','latitude','longitude','region']

class Statesadmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['name','country_id','country_code','country_name','state_code','latitude','longitude']
    list_per_page=10
    list_filter=['country_name']
    search_fields=['name','country_id','country_code','country_name','state_code','latitude','longitude']
class Citiesadmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['name','state_id','state_code','state_name','country_id','country_code','country_name','latitude','longitude']
    list_per_page=10
    list_filter=['country_name','state_name']
    # list_filter=['state_name']
    search_fields=['name','state_id','state_code','state_name','country_id','country_code','country_name','latitude','longitude']

class vendor_cat_list(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['category_name']
    list_per_page=10
    search_fields= ['category_name']

admin.site.register(models.Countries,countriesAdmin)
admin.site.register(models.States,Statesadmin)
admin.site.register(models.Cities,Citiesadmin)
class total_sales_list(admin.ModelAdmin):
    list_display=['vendor_id']
admin.site.register(models.total_sales,total_sales_list)
admin.site.register(models.vendor_categories,vendor_cat_list)
admin.site.register(models.vendor_categories_french,vendor_cat_list)
# admin.site.register(models.SampleModel)
# admin.site.register(models.ChoiceList)
class vendor_sub_cat_list(admin.ModelAdmin):
    list_display=['sub_category_name','main_category']
    search_fields=['main_category','sub_category_name']
    list_per_page = 10
    list_filter = ['main_category']
admin.site.register(models.vendor_sub_categories,vendor_sub_cat_list)
admin.site.register(models.vendor_sub_categories_french)
# admin.site.register(models.Listings_Data)
class vendor_ques_list(admin.ModelAdmin):
    list_display=['Question_Text','Question_Category']
    search_fields=['Question_Text']
    list_filter=['Question_Category']
    

class req_quote(admin.ModelAdmin):
    list_display=['fname','lname','email','event_type']
admin.site.register(models.vendor_questions,vendor_ques_list)
# admin.site.register(models.vendor_question_type)
class Vendor_Public_Packages_List(admin.ModelAdmin):
    list_display = ['package_name','Whats_Included','package_price','package_price_range_max','package_price_range_min','package_category','category_name','package_for','valid_till','created_on','vendor_id','vendor_name','location_country_code','location_state_code','attendee_range','pricing_model','image']
    search_fields = ['package_name']
    def Whats_Included(self,obj):
        return mark_safe(obj.what_included)
admin.site.register(models.vendor_public_packages,Vendor_Public_Packages_List)

class vendor_gallery_list(admin.ModelAdmin):
    list_display = ["photo_id","photo_category",'category_name','vendor_email','photo_src']

admin.site.register(models.vendor_gallery,vendor_gallery_list)
admin.site.register(models.request_a_quote,req_quote)
admin.site.register(models.total_accepted_orders)
admin.site.register(models.vendor_quote_invoice)
admin.site.register(models.total_sales_count)

class Search_CMS(admin.ModelAdmin):
    list_display = ['category_name','search_subheading','search_image']

admin.site.register(models.search_cms,Search_CMS)



class Bank_listing(admin.ModelAdmin):
    list_display=['Vendor_Id','Bank_Name','Account_Name','Bank_Account_Number','Country','Code_Banque','Code_Guichet','Cle_RIB','IBAN','Code_Swift','Domiciliation']
    # readonly_fields = ['Bank_Name','Account_Name','Bank_Account_Number','Country','Code_Banque','Code_Guichet','Cle_RIB','IBAN','Code_Swift','Domiciliation']

admin.site.register(models.Vendor_bank_listing,Bank_listing)
# admin.site.register(models.vendor_public_deals)
# admin.site.register(models.vendor_filter_answers)

class leads_package_list(admin.ModelAdmin):
    list_display = ['package_name','package_desc','package_fee','valid_type','created_at']
admin.site.register(models.vendor_leads_package,leads_package_list)


class Vendor_FAQ_List(admin.ModelAdmin):
    list_display = ['Question','status','created_at']

admin.site.register(models.Vendor_FAQ,Vendor_FAQ_List)