from django.contrib import admin
from django_admin_geomap import ModelAdmin

from .models import *
# Register your models here.

class EV_Contact_list(admin.ModelAdmin):
    list_display = ['Company_Name','Address_Line_1','Address_Line_2','City','State','Country','Phone_Number','Email']
    def has_add_permission(self, request,obj=None):
        return False
    def has_delete_permission(self, request,obj=None):
        return False
admin.site.register(EV_Contact,EV_Contact_list)
