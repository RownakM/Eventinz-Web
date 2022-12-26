from django.contrib import admin

from Mails.models import User_Welcome_Mail
from django.utils.safestring import mark_safe



# Register your models here.

class Welcome_Mail_List(admin.ModelAdmin):
    list_display = ['greeting_type','subject','Body']
    def Body(self,obj):
        return mark_safe(obj.content)

    def has_add_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False
admin.site.register(User_Welcome_Mail,Welcome_Mail_List)