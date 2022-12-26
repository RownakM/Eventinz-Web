from django import template
from content_app.models import Exchange_Rates
from transaction_records_user.models import Vendor_Payment_History, user_transaction_records
from vendor_admin.models import States,Countries, request_a_quote, vendor_quote_invoice
from numerize.numerize import numerize
from localStoragePy import localStoragePy
localStorage=localStoragePy('eventinz.com','json')
register = template.Library()
@register.filter
def gettransaction(value):
    db = Vendor_Payment_History.objects.filter(quote_id=value)
    return db


@register.filter
def getmilestoneamount(value,a):
    db = vendor_quote_invoice.objects.get(link_id=value)
    if a == '2':
        return str(float(db.total_amt) - float(db.milestone))
    else:
        return str(db.milestone)

@register.filter
def getstate(value):
    db = vendor_quote_invoice.objects.filter(link_id=value)
    if db.count() >= 2:
        return True
    else:
        return False