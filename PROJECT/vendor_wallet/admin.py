from django.contrib import admin
from vendor_wallet.models import *
# Register your models here.
class wallet_list(admin.ModelAdmin):
    list_display=['vendor_id','total_balance','remaining_balance','last_recharged_on']
admin.site.register(vendor_wallet_manager,wallet_list)