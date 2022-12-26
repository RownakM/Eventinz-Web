from django.contrib import admin
from .models import *
# Register your models here.


class Language_Control_List(admin.ModelAdmin):
    list_display=['english_text','french_text','status']

admin.site.register(Language_Control,Language_Control_List)