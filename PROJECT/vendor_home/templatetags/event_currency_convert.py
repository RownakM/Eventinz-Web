from django import template
from content_app.models import Exchange_Rates
from vendor_admin.models import States,Countries, vendor_categories
from eventmanager.models import event_entries
from localStoragePy import localStoragePy
localStorage=localStoragePy('eventinz.com','json')
register = template.Library()


@register.filter
def currency_filter(value,country):
    country_split=str(country)
    country_split1=country_split.split('/')
    vendor_country=country_split1[1]
    user_country=country_split1[3]
    amount=value

    if vendor_country == 'none':
        vendor_country = 'Benin'
    if vendor_country == 'Bénin':
        vendor_country = 'Benin'
    get_currency_vendor=Countries.objects.get(name=vendor_country).currency
   
    get_user_country=user_country
    get_user_currency=Countries.objects.get(name=get_user_country).currency
    # ex_value=Exchange_Rates.objects.get(base_country=get_currency_vendor,dest_country=get_user_currency).ex_rate


    import requests

    url = 'https://api.exchangerate.host/convert?from='+get_currency_vendor+'&to='+get_user_currency
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    
    total=round(onefcfa*amount,2)



    b=country
    # return get_currency
    from numerize.numerize import numerize
    grand=str(numerize(total))
    return grand

@register.filter
def currency_code(value,data):

    country_split=str(data)
    country_split1=country_split.split('/')
    vendor_country=country_split1[1]
    user_country=country_split1[3]
    get_user_country=user_country
    get_user_currency=Countries.objects.get(name=get_user_country).currency
    if (get_user_currency == 'XOF'):
        get_user_currency = 'F CFA'
    return get_user_currency

@register.filter
def get_vendor_type(value):
    a=value
    b=a.split(',')
    vendor_list=[]
    for i in b:
        if i =='':
            break
        vendor_data=vendor_categories.objects.get(id=i).category_name
        vendor_list.append(vendor_data)
    
    return vendor_list

@register.filter
def get_vendor_type_multi(value):
    uuid = value
    db = event_entries.objects.filter(unique_id=uuid)
    cat_name = []
    if db.exists():
        if db.count() > 0:
            for i in db:
                cat_name.append(i.vendor_type)
            
            return cat_name
        else:
            return False
    else:
        return False

@register.filter
def get_vendor_type_single(value):
    a=value
    db=vendor_categories.objects.get(id=a).category_name
    # b=a.split(',')
    # vendor_list=[]
    # for i in b:
    #     if i =='':
    #         break
    #     vendor_data=vendor_categories.objects.get(id=i).category_name
    #     vendor_list.append(vendor_data)
    
    return db