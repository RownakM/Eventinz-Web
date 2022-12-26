from django import template
from vendor_admin.models import States, Vendor_Users
from content_app.models import event_categories
from eventmanager.models import event_heads_manager, vendor_event_proposal, vendor_event_proposal_items
register = template.Library()


@register.filter
def get_list(value):
    a=''
    for i in range(1,value+1):
        a=a+str(i)
    return a