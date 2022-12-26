from django import template
from content_app.models import Exchange_Rates
from vendor_admin.models import States,Countries, Vendor_Users, vendor_public_packages, vendor_quote_invoice
from transaction_records_user.models import Vendor_Payment_History_events
from numerize.numerize import numerize
from localStoragePy import localStoragePy
localStorage=localStoragePy('eventinz.com','json')
register = template.Library()


@register.filter
def currency_filter(value,country):
    country_split=str(country)
    country_split1=country_split.split('/')
    vendor_country=country_split1[1]
    user_country=country_split1[3]
    if user_country=='':
        user_country='India'
    amount=float(value)

    if vendor_country == 'none':
        vendor_country = '24'
    
    try:

        get_currency_vendor=Countries.objects.get(id=vendor_country).currency
    except ValueError:
        get_currency_vendor=Countries.objects.get(name=vendor_country).currency

        
    get_user_country=user_country
    get_user_currency=Countries.objects.get(name=get_user_country).currency
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+get_currency_vendor

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()
    # ex_value=Exchange_Rates.objects.get(base_country=get_currency_vendor,dest_country=get_user_currency).ex_rate


    import requests
    try:
        url = 'https://api.exchangerate.host/convert?from='+get_currency_vendor+'&to='+get_user_currency
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['info']['rate'])
        
        total=round(onefcfa*amount,2)
    except ValueError:
        url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+get_currency_vendor
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['conversion_rates'][get_user_currency])
        total = round(onefcfa*amount,2)



    b=country
    try:
        grand=str(numerize(total))
    except:
        grand = str(total)
    # return get_currency
    return grand

@register.filter
def currency_code(value,data):

    country_split=str(data)
    country_split1=country_split.split('/')
    vendor_country=country_split1[1]
    user_country=country_split1[3]
    if user_country=='':
        user_country='India'
    get_user_country=user_country
    get_user_currency=Countries.objects.get(name=get_user_country).currency
    if (get_user_currency == 'XOF'):
        
        get_user_currency = 'F CFA'
    
    return get_user_currency

@register.filter
def get_milestone(value,user):
    id = value
    db = vendor_quote_invoice.objects.get(id=id)
    vendor_curr_name = db.vendor_id.country_name
    vendor_curr = Countries.objects.get(name = vendor_curr_name).currency
    user_curr = Countries.objects.get(name = user).currency

    milestone = float(db.milestone)
    
    
    if milestone > 0:
        import requests

        url = 'https://api.exchangerate.host/convert?from='+vendor_curr+'&to='+user_curr
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['info']['rate'])
        total=round(onefcfa*milestone,2)
        return total
    else:
        return 0

@register.filter
def get_tax(value,user):
    id=value
    db = vendor_quote_invoice.objects.get(id=id)
    vendor_curr_name = db.vendor_id.country_name
    vendor_curr = Countries.objects.get(name = vendor_curr_name).currency
    user_curr = Countries.objects.get(name = user).currency
    tax = float(db.tax_percent)
    amount = float(db.total_amt)
    if tax > 0:
        import requests
        url = 'https://api.exchangerate.host/convert?from='+vendor_curr+'&to='+user_curr
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['info']['rate'])
        total=round(onefcfa*((tax*amount)/100),2)
        return total 
    else:
        return 0

@register.filter
def get_total(value,user):
    id = value
    tax = get_tax(value,user)
    db = vendor_quote_invoice.objects.get(id=id)
    amount = float(db.total_amt)
    vendor_curr_name = db.vendor_id.country_name
    vendor_curr = Countries.objects.get(name = vendor_curr_name).currency
    user_curr = Countries.objects.get(name = user).currency
    if amount > 0:
        import requests

        url = 'https://api.exchangerate.host/convert?from='+vendor_curr+'&to='+user_curr
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['info']['rate'])
        total=round(onefcfa*amount,2)+round(tax,2)
        return numerize(total)
    else:
        return 0

@register.filter
def is_vendor_have_pricing(value):
    db = Vendor_Users.objects.get(id=value)
    if (float(db.max_budget) > 0 and float(db.min_budget) > 0):
        return 'pricing_yes'
    else:
        return 'pricing_no'

@register.filter
def is_vendor_have_package(value):
    user = Vendor_Users.objects.get(id=value).Email
    db = vendor_public_packages.objects.filter(vendor_id=user)
    if db.exists():
        return 'package_yes'
    else:
        return 'package_no'

@register.filter
def is_finalise_enabled(value):
    db = Vendor_Payment_History_events.objects.filter(event_id__id=value)
    if db.exists():
        status = False
        for i in db:
            if i.status != 'Paid':
                status = False
                break
            else:
                status = True
        return status
    else:
        return False