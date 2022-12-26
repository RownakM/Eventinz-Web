from django.contrib import admin
from .models import Vendor_Payment_History, Vendor_Payment_History_events, user_transaction_records
# Register your models here.
class user_trans_list(admin.ModelAdmin):
    list_display = ["quote_id",'transaction_id','transaction_type','transaction_amount','remarks','email']

class Vendor_Payment_History_list(admin.ModelAdmin):
    list_display = ['vendor_id','quote_id','host_id','Bank_Name','Account_Name','Bank_AC_Number','Country','Bank_Reference_Code','Depositor_Name','Payment_By','Transaction_File_Record','tran_num','amount','created_at']

class Vendor_Payment_History_Event_List(admin.ModelAdmin):
    list_display = ['vendor_id','event_id','host_id','Bank_Name','Account_Name','Bank_AC_Number','Amount','Transaction_File_Record','created_at','status']

admin.site.register(user_transaction_records,user_trans_list)
admin.site.register(Vendor_Payment_History,Vendor_Payment_History_list)
admin.site.register(Vendor_Payment_History_events,Vendor_Payment_History_Event_List)