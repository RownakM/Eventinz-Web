from django.db import models
from user_dashboard.models import user_login
from vendor_admin.models import Vendor_Users, request_a_quote, vendor_quote_invoice
from eventmanager.models import *
# Create your models here.
class user_transaction_records(models.Model):
    quote_id=models.ForeignKey(request_a_quote,on_delete=models.CASCADE)
    transaction_id=models.CharField(max_length=4000)
    transaction_type=models.CharField(max_length=400)
    transaction_amount=models.CharField(max_length=300)
    remarks=models.CharField(max_length=300,default='1')
    email=models.CharField(max_length=300,default='0')
    class Meta:
        verbose_name_plural = "User Transaction Records"


class Vendor_Payment_History(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    quote_id=models.ForeignKey(request_a_quote,on_delete=models.CASCADE)
    
    host_id=models.ForeignKey(user_login,on_delete=models.CASCADE)
    Bank_Name=models.CharField(max_length=1000)
    Account_Name=models.CharField(max_length=4000)
    Bank_AC_Number=models.CharField(max_length=4000)
    Country = models.CharField(max_length=1000)
    Bank_Reference_Code=models.CharField(max_length=4000)
    Depositor_Name=models.CharField(max_length=2000)
    Payment_By=models.CharField(max_length=4000)
    Transaction_File_Record=models.FileField(upload_to='transaction_records_user/user_data/')
    tran_num = models.CharField(max_length = 100,default="1")
    created_at = models.DateTimeField(auto_now_add = True)
    amount = models.IntegerField(default = 0)

    class Meta:
        verbose_name_plural = "Vendor Payment History"

class Vendor_Payment_History_events(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    event_id=models.ForeignKey(event_entries,on_delete=models.CASCADE)
    
    host_id=models.ForeignKey(user_login,on_delete=models.CASCADE)
    Bank_Name=models.CharField(max_length=1000)
    Account_Name=models.CharField(max_length=4000)
    Bank_AC_Number=models.CharField(max_length=4000)
    Amount=models.CharField(max_length=4000)
    # Country = models.CharField(max_length=1000)
    # Bank_Reference_Code=models.CharField(max_length=4000)
    # Depositor_Name=models.CharField(max_length=2000)
    # Payment_By=models.CharField(max_length=4000)
    Transaction_File_Record=models.FileField(upload_to='transaction_records_user/events/user_data/')
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=5000,default="Pending Verification")
    class Meta:
        verbose_name_plural = "Vendor Payment History - Events" 