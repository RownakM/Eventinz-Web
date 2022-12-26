from django import template
from content_app.models import Exchange_Rates
from vendor_admin.models import States,Countries
from numerize.numerize import numerize
from localStoragePy import localStoragePy
localStorage=localStoragePy('eventinz.com','json')
register = template.Library()
@register.filter
def userlogin(value):
    if value == '' or value == None:
        return False
    else:
        return True