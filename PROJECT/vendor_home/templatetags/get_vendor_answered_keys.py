# bank_details=Vendor_bank_listing.objects.filter(Vendor_Id=id)
from django import template
from vendor_admin.models import States, Vendor_Users, Vendor_bank_listing, vendor_categories, vendor_filter_answers
from content_app.models import event_categories
from eventmanager.models import event_heads_manager
register = template.Library()
@register.filter
def get_check(value,email):
    db=vendor_filter_answers.objects.filter(vendor_id=Vendor_Users.objects.get(Email=email).id,question_id=value)
    if db.exists() :
        return "Check"
    else:
        return "No"
