from import_export.admin import ImportExportModelAdmin
from admin_totals.admin import ModelAdminTotals
from django.db.models.functions import Coalesce
from django.db.models import Sum, Avg
from currency_symbols import CurrencySymbols
from numerize import numerize
from django.contrib import admin
from django.utils.safestring import mark_safe


from import_export import resources
# Register your models here.
from .models import *
class EV_About_list(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['Header_Text','Header_subtext','Header_Background','Who_We_Are','Who_We_Are_Sub_Heading','Who_We_Are_Image','Mission_Text','Mission_Sub_Text','Action']
    list_display_links=['Action']
    
    def Who_We_Are(self,obj):
        return mark_safe(obj.Who_We_Are_Heading)
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request , obj=None):
        return False
    def Action(self,obj):
        return 'Change'
    
class Ev_Teams_List(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['Full_Name','Designation','linkedin_url','Action']
    list_display_links=['Action']
    search_fields=['Full_Name','Designation','linkedin_url']
    
    def Action(self,obj):
        return 'Change'
    
admin.site.register(EV_About,EV_About_list)
admin.site.register(Eventinz_Teams,Ev_Teams_List)