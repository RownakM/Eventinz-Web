from django import template
from content_app.models import Exchange_Rates
from vendor_admin.models import States,Countries
from localStoragePy import localStoragePy
localStorage=localStoragePy('eventinz.com','json')
register = template.Library()


@register.filter
def usd_convert(value,user_currency):
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+user_currency

    # ex_value=Exchange_Rates.objects.get(base_country=user_currency,dest_country='USD').ex_rate
    # onefcfa=float(ex_value)
        # Making our request
    import requests

    url = 'https://api.exchangerate.host/convert?from='+user_currency+'&to=USD'
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    
    total=round(onefcfa*float(value),2)
    return total