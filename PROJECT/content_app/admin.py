from import_export.admin import ImportExportModelAdmin
from admin_totals.admin import ModelAdminTotals
from django.db.models.functions import Coalesce
from django.db.models import Sum, Avg
from currency_symbols import CurrencySymbols
from numerize import numerize
from django.contrib import admin
from content_app.models import *
from django.utils.safestring import mark_safe

# Register your models here.

class event_list(admin.ModelAdmin):
    list_display=['sub_category_name','category']
class exchange_rates_list(admin.ModelAdmin):
    list_display=['base_country','dest_country','ex_rate']
    list_per_page=5
    list_filter=['base_country','dest_country']
    search_fields=['base_country','dest_country']
class venue_details_list(admin.ModelAdmin):
    list_display=['venue_name']
class cron_filter(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['cron_type','cron_purpose','start_time','end_time','status']
    list_display_links=None


class event_categories_custom(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['category_name','Action']
    list_display_links=['Action']
    list_per_page=5

    
    def Action(self,obj):
        return 'Change'
class Exchange_Rate_API_list(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['email','apikey','Action']
    list_display_links=['Action']

    def Action(self,obj):
        return 'Change'

class Our_Vendor_Class(admin.ModelAdmin):
    list_display=['Header_Text','Display_text','background_image']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request , obj=None):
        return False
    

admin.site.register(Our_Vendor_CMS,Our_Vendor_Class)
# admin.site.register(Exchange_Rates_API,Exchange_Rate_API_list)
# admin.site.register(cron_activities,cron_filter)

admin.site.register(event_categories,event_categories_custom)
# admin.site.register(event_categories_french)
admin.site.register(event_sub_categories,event_list)
# admin.site.register(event_sub_categories_french,event_list)
admin.site.register(Venue_Type)
admin.site.register(Venue_Details,venue_details_list)
admin.site.register(Venue_Type_by_venue)

class Venue_Main(admin.ModelAdmin):
    list_display=['venue_header','venue_by_venue','venue_by_venue_subheading','venue_by_event','venue_by_event_subheading','image']
    def image(self,obj):
        return mark_safe('<a href="/media/%s"><i class="fas fa-eye text-success"></i></a>' % (obj.venue_head_image))
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request , obj=None):
        return False
admin.site.register(Venue_main_home,Venue_Main)
# admin.site.register(Exchange_Rates,exchange_rates_list)
