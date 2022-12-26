from django import template
from vendor_admin.models import States, Vendor_Users
from content_app.models import event_categories
from eventmanager.models import event_heads_manager
register = template.Library()


@register.filter
def vendor_name(value):
    db=Vendor_Users.objects.get(Email=value)
    
    cname = db.Company_Name

    return cname

@register.filter
def vendor_id(value):
    db=Vendor_Users.objects.get(Email=value)
    id=db.id
    return id

@register.filter
def vendor_name_by_id(value):
    db = Vendor_Users.objects.get(id=value).Company_Name
    return db