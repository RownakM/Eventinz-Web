# bank_details=Vendor_bank_listing.objects.filter(Vendor_Id=id)
from django import template
from vendor_admin.models import States, Vendor_bank_listing, vendor_categories
from content_app.models import event_categories
from eventmanager.models import event_heads_manager
register = template.Library()
@register.filter
def get_v_vat(value):
    cat=vendor_categories.objects.get(id=value).category_name
    return cat

@register.filter
def getvList(value):
    a = value
    b = a.split(",")
    return b