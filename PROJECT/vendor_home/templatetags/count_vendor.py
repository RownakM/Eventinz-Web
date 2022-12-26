from django import template
from vendor_admin.models import States, Vendor_Users
register = template.Library()


@register.filter
def count_vendor_num(value):
    vendor=Vendor_Users.objects.filter(vendor_categories__has_key=value).count()

    return str(vendor)+' '+str(value)