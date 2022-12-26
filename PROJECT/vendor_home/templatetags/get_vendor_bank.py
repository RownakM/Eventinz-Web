# bank_details=Vendor_bank_listing.objects.filter(Vendor_Id=id)
from django import template
from vendor_admin.models import States, Vendor_bank_listing
from content_app.models import event_categories
from eventmanager.models import event_heads_manager
register = template.Library()


@register.filter
def get_bank(value):
    bank_details=Vendor_bank_listing.objects.filter(Vendor_Id=value)
    return bank_details