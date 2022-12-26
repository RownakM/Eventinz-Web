from django import template
from vendor_admin.models import States
register = template.Library()


@register.filter
def country_filter(value):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    import requests
    country=value

    url = "https://api.countrystatecity.in/v1/countries/"+country

    headers = {
        'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    }

    response = requests.request("GET", url, headers=headers)

    # print(response.text)
    import json
    data=json.loads(response.text)
    get_country=data['name']
    return get_country

@register.filter
def state_filter(value,country):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    # import requests
    # country=value

    # url = "https://api.countrystatecity.in/v1/countries/"+country

    # headers = {
    #     'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    # }

    # response = requests.request("GET", url, headers=headers)

    # # print(response.text)
    # import json
    # data=json.loads(response.text)
    import requests
    country_data=country
    state=value
    url = "https://api.countrystatecity.in/v1/countries/"+country_data+"/states/"+state

    headers = {
        'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    }

    response = requests.request("GET", url, headers=headers)

    # print(response.text)
    import json
    data=json.loads(response.text)
    get_state=data['name']
    return get_state

@register.filter
def key(d, key_name):
    return d[key_name]