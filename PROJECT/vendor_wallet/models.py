from django.db import models
from vendor_admin.models import Vendor_Users
# Create your models here.
class vendor_wallet_manager(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    total_balance=models.CharField(max_length=400)
    remaining_balance=models.CharField(max_length=400)
    last_recharged_on=models.DateField()