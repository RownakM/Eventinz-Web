from django import template
from vendor_admin.models import States
from content_app.models import event_categories
from eventmanager.models import event_heads_manager
register = template.Library()


@register.filter
def head_find(value):
    cat=event_heads_manager.objects.get(id=value)
    mini=cat.Minimum_Value
    maxi=cat.Maximum_Value
    output=str(mini) + ' - '+ str(maxi)
    return output