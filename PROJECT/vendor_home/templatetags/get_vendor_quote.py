from django import template
from vendor_admin.models import States, Vendor_Users
from content_app.models import event_categories
from eventmanager.models import event_heads_manager, vendor_event_proposal, vendor_event_proposal_items
register = template.Library()


@register.filter
def get_event_quotation(value):
    id=value
    db=vendor_event_proposal_items.objects.filter(proposal_id=id)
    return db