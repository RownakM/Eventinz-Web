from django.contrib import admin
from indexCMS.models import *
# Register your models here.
class index_header_list(admin.ModelAdmin):
    list_display=['Header','sub_header']
    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False

class eventinz_works(admin.ModelAdmin):
    list_display=['Header_Text','Sub_Text','Step_1_Text','Step_2_Text','Step_3_Text']
    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False

class adv_list(admin.ModelAdmin):
    list_display=['adv_heading','adv_subtext']
    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False

class index_slider_view(admin.ModelAdmin):
    list_display=['image']
    

class Vendor_Deals_List(admin.ModelAdmin):
    list_display=['heading','sub_heading','Package_Button_Text','Deals_Button_Text']
admin.site.register(index_headers,index_header_list)
admin.site.register(index_slider,index_slider_view)
admin.site.register(how_eventinz_works,eventinz_works)
admin.site.register(advertisement,adv_list)
admin.site.register(Vendor_Deals_Index_CMS,Vendor_Deals_List)

class Vendor_Category_List(admin.ModelAdmin):
    list_display = ['Heading','Sub_Heading']
    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False

admin.site.register(Vendor_Categories_Text,Vendor_Category_List)

admin.site.register(Packages_CMS)