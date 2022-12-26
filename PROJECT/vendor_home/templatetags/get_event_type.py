from django import template
from eventmanager.models import event_heads_manager, vendor_event_proposal
from vendor_admin.models import States
from content_app.models import event_categories,event_sub_categories
from eventmanager.models import event_entries
register = template.Library()


@register.filter
def event_type(value):
    cat=event_categories.objects.get(id=value).category_name
    return cat
@register.filter
def is_bid(ev_id,ven_id):
    db = vendor_event_proposal.objects.filter(vendor_id=ven_id,event_id=ev_id)
    if db.exists() > 0:
        return True
    else:
        return False

@register.filter
def minimum_heads(id):
    db = event_heads_manager.objects.get(id=id).Minimum_Value
    return db

@register.filter
def maximum_heads(id):
    db = event_heads_manager.objects.get(id=id).Maximum_Value
    return db

@register.filter
def get_event_sub_categories(item):
    obj = item
    obj_new=obj.replace('[','').replace(']','').replace('"','').split(',')
    sub_name=[]
    for i in obj_new:
        db = event_sub_categories.objects.get(id=int(i)).sub_category_name
        sub_name.append(db)
        
    return sub_name
