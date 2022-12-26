from django import template
from vendor_admin.models import States, Vendor_Users, vendor_filter_answers, vendor_subscription
register = template.Library()

@register.filter()
def get_vendor_features(value):
    id=value
    get_vendor_question=vendor_filter_answers.objects.filter(vendor_id=id)
    return get_vendor_question

@register.filter()
def is_enterprise(value):
    id = value
    get_vendor_profile = Vendor_Users.objects.get(id=id)
    if get_vendor_profile.package == 'Standard' or get_vendor_profile.package == '' or get_vendor_profile.package == None:
        return False
    else:
        return True
    