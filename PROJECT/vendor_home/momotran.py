def MTNMoMoSandboxuser(API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    import uuid
    storeid=str(uuid.uuid4())
    headers = {
        # Request headers
        'X-Reference-Id': str(storeid),
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    requestbody="{'providerCallbackHost': 'webhook.site'}"
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/v1_0/apiuser?%s" % params, requestbody, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        #print(response.status) # 201 - OK
        #print(storeid)
        return str(storeid)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def MTNMoMoSandboxuser_GetUser(xrefid,API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("GET", "/v1_0/apiuser/"+str(xrefid)+"?%s" % params, "{}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        #print(response.status) # 200 - OK
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def MTNMoMoSandboxuser_CreateAPIKeyForUser(xrefid,API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64,json

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/v1_0/apiuser/"+str(xrefid)+"/apikey?%s" % params, "{}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        x=json.loads(data)
        apikey=str(x['apiKey'])
        
        conn.close()
        return apikey
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def createAccessToken(xrefid,apikey,API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64,json
    sample_string = xrefid+":"+apikey
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    headers = {
        # Request headers
        'Authorization': 'Basic '+base64_string,
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/collection/token/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        x=json.loads(data)
        access_token=str(x['access_token'])
        conn.close()
        return access_token
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def sendrequesttopay(Authorisation,xrefid,xtenv,API_KEY,amount,mobile,currency):
    import http.client, urllib.request, urllib.parse, urllib.error, base64,json

    headers = {
        # Request headers
        'Authorization': 'Bearer '+Authorisation,
        'X-Callback-Url': 'https://webhook.site/eee2c577-71cf-47a7-8517-ed9b195bad58',
        'X-Reference-Id': xrefid,
        'X-Target-Environment': xtenv,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': API_KEY,
    }
    requestbody=str({
  "amount": amount,
  "currency": currency,
  "externalId": "12567890",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": mobile
  },
  "payerMessage": "payermsg",
  "payeeNote": "payernote"
})
    # print(requestbody)
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, requestbody, headers)
        response = conn.getresponse()
        data = response.read()
        
        #print(data)
        #print(response.status)
        #print(response.msg)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def get_transaction_status(requesttopay_uuid,create_accesstoken,xtenv,API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Authorization': 'Bearer '+create_accesstoken,
        'X-Target-Environment': xtenv,
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("GET", "/collection/v1_0/requesttopay/"+requesttopay_uuid+"?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        import json
        status = json.loads(data)
        
        # print(data)
        # print("="*40)
        conn.close()
        return status
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_acc_balance(create_accesstoken,xtenv,API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Authorization': 'Bearer '+create_accesstoken,
        'X-Target-Environment': xtenv,
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("GET", "/collection/v1_0/account/balance?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def get_acc_holder_status(accid,xtenv,create_accesstoken,API_KEY):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Authorisation':'Bearer '+create_accesstoken,
        'X-Target-Environment': xtenv,
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("GET", "/collection/v1_0/accountholder/msisdn/"+accid+"/active?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        #print(response.status)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
API_KEY='269abdb04bbb48009820e0553a0311b0'
import uuid

import time


# amount=str(input("Enter Amount : "))
# mobile=str(input("Enter Mobile : "))
# currency=str(input("Enter Currency : "))

def main_call(amount,mobile,currency):
    genuuid=MTNMoMoSandboxuser(API_KEY)
    getuser=MTNMoMoSandboxuser_GetUser(str(genuuid),API_KEY)
    userapikey=MTNMoMoSandboxuser_CreateAPIKeyForUser(str(genuuid),API_KEY)
    create_accesstoken=createAccessToken(str(genuuid),userapikey,API_KEY)
    requesttopay_uuid=str(uuid.uuid4())
    requesttopay=sendrequesttopay(str(create_accesstoken),requesttopay_uuid,'sandbox',API_KEY,amount,mobile,currency)
    # print("Checking after 30 seconds")
    time.sleep(15)
    gettranstatus=get_transaction_status(requesttopay_uuid,str(create_accesstoken),'sandbox',API_KEY)
    return gettranstatus
    #getaccbal=get_acc_balance(str(create_accesstoken),'sandbox',API_KEY)
    # accid="1234092912"
    #get_acc_status=get_acc_holder_status(accid,'sandbox',str(create_accesstoken),API_KEY)

# print("CALLING")


# print("CALLED")


def generate_token_live():
    import requests
    import json
    url = "https://proxy.momoapi.mtn.com/collection/token/"

    payload={}
    headers = {
    'Ocp-Apim-Subscription-Key': '5e326653617049d09df313c92618202b',
    'Authorization': 'Basic N2FlMmE5ZDEtZDA2My00MjkwLWFiNWItNmVlZTVkMjYzOGJjOjUyYTU2ZGJlMDIyYzRjMDU4ODAzYjI2MWE0ZDk0NWNm'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    access_token = json_data['access_token']
    # print(access_token)
    return access_token

def request_to_pay(amount,mobile,currency,payment_x_ref_id,access_token):
    import requests
    import json
    # import uuid

    url = "https://proxy.momoapi.mtn.com/collection/v1_0/requesttopay"

    payment_X_reference_id = payment_x_ref_id
    payload = json.dumps({
    "amount": str(amount),
    "currency": "XOF",
    "externalId": payment_X_reference_id,
    "payer": {
        "partyIdType": "MSISDN",
        "partyId": str(mobile)
    },
    "payerMessage": "Eventinz - Payments",
    "payeeNote": "Payment to Eventinz"
    })
    headers = {
    'X-Reference-Id': payment_X_reference_id,
    'X-Target-Environment': 'mtnbenin',
    'Ocp-Apim-Subscription-Key': '5e326653617049d09df313c92618202b',
    'Authorization': 'Bearer '+str(access_token),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    result = response.status_code
    # print(result)
    return result
    
def check_payment_status(payment_x_ref_id,access_token):
    import requests
    import json
    url = "https://proxy.momoapi.mtn.com/collection/v1_0/requesttopay/"+str(payment_x_ref_id)

    payload={}
    headers = {
    'X-Target-Environment': 'mtnbenin',
    'Ocp-Apim-Subscription-Key': '5e326653617049d09df313c92618202b',
    'Authorization': 'Bearer '+str(access_token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    print(json_response)
    if json_response['status'] == "FAILED":
        return False
    elif json_response['status'] == "SUCCESSFUL":
        return True
    else:
        return False
    


def main_call_live(amount,mobile,currency):
    import time
    payment_x_ref_id = str(uuid.uuid4())
    access_token = generate_token_live()
    time.sleep(2)
    requesttopay = request_to_pay(str(amount),str(mobile),str(currency),payment_x_ref_id,access_token)
    time.sleep(3)
    if requesttopay == 200 or requesttopay == 202:
        time.sleep(45)
        payment_status = check_payment_status(payment_x_ref_id,access_token)
        if payment_status == False:
            # return str(payment_x_ref_id)+"Access"+str(access_token)
            return False
        elif payment_status == True:
            return True
        else:
            return payment_status

    else:
        return requesttopay
        
# main_call_live("100","22954335133","XOF")
