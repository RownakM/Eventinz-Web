from about.models import *
from .admin import Exchange_Rate_API_list
from content_app.models import Exchange_Rates, Exchange_Rates_API,cron_activities
from vendor_admin.models import vendor_quote_invoice
import cronitor
import datetime
cronitor.api_key = '807bc634acb9428b86ecde052949fdbc'

@cronitor.job('exchange_rate_monitor')
def exchange_rates_view():
    start_time=datetime.datetime.now()
    Exchange_Rates.objects.all().delete()
    
    import requests
    import json
    import time
    time.sleep(4)
    # return HttpResponse("")
    url = "https://api.countrystatecity.in/v1/countries"

    headers = {
    'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    }

    response = requests.request("GET", url, headers=headers)

    data=response.text
    data_json=json.loads(data)
    count=0
    count_error=0
    currency_list=[]
    for i in data_json:
        country_name=i['iso2']
        # print("="*100)
        # print(i['name'])
        # print("="*100)
        # time.sleep(4)
        url = "https://api.countrystatecity.in/v1/countries/"+country_name
        
        response = requests.request("GET", url, headers=headers)
        data_country_details=response.text
        data_country_details_json=json.loads(data_country_details)
        data_country_details_json_currency=data_country_details_json['currency']
        if data_country_details_json_currency not in currency_list:
            currency_list.append(data_country_details_json_currency)
            get_random_api=Exchange_Rates_API.objects.order_by('?').first()
            api_key=get_random_api.apikey
            url = 'https://v6.exchangerate-api.com/v6/'+api_key+'/latest/'+data_country_details_json['currency']

                # Making our request
            response = requests.get(url)
            data_conversion_rates = response.json()
            base_currency = data_country_details_json['currency']
            try:
                
                rates = data_conversion_rates['conversion_rates']
                count_x=0
                for i , j in rates.items():
                    # print("Base Currency : ",base_currency,"\tDestination Currency :",i,"\tExchange Rate : ",j)
                    obj, created = Exchange_Rates.objects.get_or_create(
                        base_country=base_currency,
                        dest_country=i,
                        ex_rate=j,
                    )
                    if created:
                        obj.save()
                    count_x+=1
            
                count+=1
            except KeyError:
                count_error+=1
                # print(data_country_details_json['currency'])
                # print(data_conversion_rates)
        #print(rates.items())
        else:
            continue
    end_time=datetime.datetime.now()
    cron_type='Job'
    cron_purpose='Exchange Rate Update'
    status = 'completed'

    cron_activities(start_time=start_time,end_time=end_time,cron_type=cron_type,cron_purpose=cron_purpose,status=status).save()

    # print(count)
    # print("Error : ",count_error)
    # print(count_x)

import requests
import json

def scheduled_delete_quotes():
    from datetime import datetime
    start_time=datetime.datetime.now()

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": "3a4f2d5bab6d4138810cd46a159dee15",
    
    }
    vendor_quotes=vendor_quote_invoice.objects.filter(valid_till__lt=datetime.now())
    for i in vendor_quotes:
        link=i.short_link
        id=i.quote_id
        requestHeaders = {
            "Content-type": "application/json",
            "apikey": "3a4f2d5bab6d4138810cd46a159dee15",
            
            }
        
        linkRequest = {
            "destination": "https://eventinz.com/staging/invoice/?quote_id="+str(id)
            , "domain": { "fullName": "link.eventinz.com" }
            , "slashtag": str(id)
            , "title": "EV/"+str(id)
            }
            
        linkRequest1=''
        # r = requests.delete("https://api.rebrandly.com/v1/links/"+str(id),data = json.dumps(linkRequest),headers=requestHeaders) 
        j =requests.get("https://api.rebrandly.com/v1/links",headers=requestHeaders)

        json_data=json.loads(j.text)
        count=0
        if (j.status_code == requests.codes.ok):
            # print("OK")
            # print()
            for z in json_data:
                # print(z)
                if z['slashtag']==str(id):
                    uid=z['id']
                    # print("FOUND")
                    r = requests.delete("https://api.rebrandly.com/v1/links/"+str(uid),headers=requestHeaders) 
                    vendor_quotes.delete()
                    
                count+=1
        else:
            print(j.status_code)
    end_time=datetime.datetime.now()
    cron_type='Job'
    cron_purpose='Expired Quote Deletion'
    status = 'completed'

    cron_activities(start_time=start_time,end_time=end_time,cron_type=cron_type,cron_purpose=cron_purpose,status=status).save()



# def newsletter_cron():
#     get_current_newsletter=
        

        
            