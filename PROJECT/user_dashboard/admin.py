from sqlite3 import ProgrammingError
import pycountry
from django.contrib import admin
from eventmanager.models import event_entries
from user_dashboard import models
from vendor_admin.models import request_a_quote
from django.db.models import Avg

# Register your models here.
class user_login_list(admin.ModelAdmin):
    list_display=['First_Name','Last_Name','Email','Country_Code','Mobile','Country','State','Total_Events','Events_On_Going','Events_Cancelled','Events_Successfull','Total_Quote_Request','Average_Number_Of_Guests']
    list_filter=['country']
    search_fields=['Email']

    def First_Name(self,obj):
        return obj.fname
    def Last_Name(self,obj):
        return obj.lname
    def Country_Code(self,obj):
        return obj.mobile_code
    def Mobile(self,obj):
        return obj.mobile
    def Country(self,obj):
        country=obj.country
        try:
            name = pycountry.countries.get(alpha_2=country).name
        except AttributeError:
            name=obj.country
        return name

    def State(self,obj):
        country = obj.country
        state = obj.state

        q=country+'-'+state

        try:
            name=pycountry.subdivisions.get(code=q).name
        except AttributeError:
            name = obj.state
        return name

    def Total_Events(self,obj):
        Email=obj.Email
        db=event_entries.objects.filter(Email=Email).count()
        return db
    
    def Events_On_Going(self,obj):
        Email=obj.Email
        db=event_entries.objects.filter(Email=Email,status='Hired').count()
        return db
    
    def Events_Cancelled(self,obj):
        Email=obj.Email
        db=event_entries.objects.filter(Email=Email,status='cancel').count()
        return db
    def Events_Successfull(self,obj):
        Email=obj.Email
        db=event_entries.objects.filter(Email=Email,status = 'Complete').count()
        return db
    def Ratings(self,obj):
        return '0'
    
    def Total_Quote_Request(self,obj):
        email=obj.Email
        db=request_a_quote.objects.filter(email=email).count()
        return db

    def Average_Number_Of_Guests(self,obj):
        email=obj.Email
        try:
            db=request_a_quote.objects.filter(email=email).values_list('no_of_guests',flat=True)
            test_list=[]
            test_list = [int(i) for i in db]
            try:
                
                a = round(sum(test_list)/len(db),2)
            except ZeroDivisionError:
                a = '0'
        except ProgrammingError:
            db='No Data'
            a = 'No Data'
        except ValueError:
            a = 'Value Error'
        return a
admin.site.register(models.user_login,user_login_list)
