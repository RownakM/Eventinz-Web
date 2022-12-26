from django.contrib import admin

# Register your models here.
from eventmanager import models
from django.utils.safestring import mark_safe


class event_entries_list(admin.ModelAdmin):
    list_display=['Email','First_Name','Last_Name','Heads','DOE','user_type','package_type','created_on']

admin.site.register(models.event_entries,event_entries_list)

class event_planner_CMS_list(admin.ModelAdmin):
    list_display = ['title','image','heading','sub_heading']
    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.event_planner_CMS,event_planner_CMS_list)

class event_heads_manager_list(admin.ModelAdmin):
    list_display = ['Minimum_Guest','Maximum_Guest']
    def Minimum_Guest(self,obj):
        return obj.Minimum_Value
    def Maximum_Guest(self,obj):
        return obj.Maximum_Value

admin.site.register(models.event_heads_manager,event_heads_manager_list)

class event_budget_settings_list(admin.ModelAdmin):
    list_display = ['country','Minimum_Budget','Maximum_Budget']
    def Minimum_Budget(self,obj):
        return obj.Minimum_Value
    def Maximum_Budget(self,obj):
        return obj.Maximum_Value
admin.site.register(models.event_budget_settings,event_budget_settings_list)

class create_event_packages_list(admin.ModelAdmin):
    list_display = ['currency_country','premium_amount','Premium_Features','Freemium_Features']
    def Freemium_Features(self,obj):
        return mark_safe(obj.freemium_features)
    def Premium_Features(self,obj):
        return mark_safe(obj.premium_features)
    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False
admin.site.register(models.create_event_packages,create_event_packages_list)



# admin.site.register(models.vendor_event_proposal_items)
# admin.site.register(models.vendor_event_proposal)