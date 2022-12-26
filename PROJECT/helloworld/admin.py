from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from helloworld.models import About, Entries, Header, Mail_User, Mail_Vendor, NewsLetter, Schedule_Mails

class Entrie_list(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['fname','lname','country','email','mobile','User_Type','created_on']
    list_per_page = 5
    list_filter=['User_Type','country']
    search_fields = ['fname','lname','country' ,'email', 'mobile','User_Type']

class NewsLetter_List(admin.ModelAdmin):
    list_display=['email','created_on','get_status']
    def get_status(self, obj):
        if obj.subscribe_status == '0':
            return "Subscribed"
        else:
            return 'Un-Subscribed'
admin.site.register(Entries,Entrie_list)
admin.site.register(About)
admin.site.register(Mail_User)
admin.site.register(Mail_Vendor)
admin.site.register(Header)
admin.site.register(NewsLetter,NewsLetter_List)
admin.site.register(Schedule_Mails)