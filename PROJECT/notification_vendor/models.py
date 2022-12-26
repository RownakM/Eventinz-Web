from django.db import models
from vendor_admin.models import Vendor_Users
from user_dashboard.models import user_login
# Create your models here.
class notification(models.Model):
    vendor_id=models.ForeignKey(Vendor_Users,on_delete=models.CASCADE)
    notification_type=models.CharField(max_length=400)
    user=models.ForeignKey(user_login,on_delete=models.CASCADE)