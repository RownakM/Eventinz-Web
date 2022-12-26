from django import template
from vendor_admin.models import States, Vendor_Users
from content_app.models import event_categories
from eventmanager.models import event_entries, event_heads_manager, vendor_event_proposal
register = template.Library()


@register.filter
def count_proposal(value):
    db=vendor_event_proposal.objects.filter(event_id=value).count()
    return db

@register.filter
def count_proposal_v2(value):
    db=vendor_event_proposal.objects.filter(event_id__unique_id=value).count()
    return db

@register.filter
def get_button_links(value):
    db = vendor_event_proposal.objects.filter(event_id__unique_id = value).distinct('event_id__vendor_type')
    return db