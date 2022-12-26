from django.contrib import admin
from .models import Eventinz_Terms,Eventinz_Privacy_Policy
# Register your models here.
from django.utils.safestring import mark_safe

class Eventinz_Terms_list(admin.ModelAdmin):
    list_display=['page_header','Content','page_image']
    def has_add_permission(self, request,obj=None):
        return False
    def has_delete_permission(self, request,obj=None):
        return False
    def Content(self,obj):
        return mark_safe(obj.content)
class Eventinz_Terms_list(admin.ModelAdmin):
    list_display=['page_header','Content','page_image']
    def has_add_permission(self, request,obj=None):
        return False
    def has_delete_permission(self, request,obj=None):
        return False
    def Content(self,obj):
        return mark_safe(obj.content)

admin.site.register(Eventinz_Terms,Eventinz_Terms_list)
admin.site.register(Eventinz_Privacy_Policy,Eventinz_Terms_list)
