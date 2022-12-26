import xmltodict, json
reqUrl="https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"
def checkMSISDN(MSISDN):
    import requests

    # reqUrl = "https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/xml" 
    }

    payload = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="http://api.merchant.tlc.com/">\n <soapenv:Header/>\n <soapenv:Body>\n <api:getMobileAccountStatus>\n \n <token>5x6HzkGQz9cBfj6eO3n/rG0alcD8rIkXwWWBzl67LnwMhReWihY9SNcHXEX2H4r4</token>\n \n <request>\n <msisdn>'+str(MSISDN)+'</msisdn>\n </request>\n </api:getMobileAccountStatus>\n </soapenv:Body>\n</soapenv:Envelope>'

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList,verify=False)
    response_obj = xmltodict.parse(response.text)
    # response_json = json.loads(response_obj)
    status = response_obj['soap:Envelope']['soap:Body']['ns2:getMobileAccountStatusResponse']['return']['subscriberstatus'] 
    if status == "ACTIVE":
        return True
    else:
        return False
    
def sendPayRequest(MSISDN,UUID_UPPER,AMOUNT):
    import requests

    # reqUrl = "https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/xml" 
    }

    payload = '''<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    \n <SOAP-ENV:Header/>
    \n <S:Body>
    \n <ns2:Push xmlns:ns2="http://api.merchant.tlc.com/">
    \n <token>5x6HzkGQz9cBfj6eO3n/rG0alcD8rIkXwWWBzl67LnwMhReWihY9SNcHXEX2H4r4</token>
    \n <msisdn>'''+str(MSISDN)+'''</msisdn>
    \n <message>TEST</message>
    \n <amount>'''+str(AMOUNT)+'''</amount>
    \n <externaldata1>'''+str(UUID_UPPER)+'''</externaldata1>
    \n <fee>0</fee>
    \n </ns2:Push>
    \n </S:Body>
    \n</S:Envelope>'''

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList,verify=False)
    response_obj = xmltodict.parse(response.text)
    # response_json = json.loads(response_obj)
    status = response_obj['soap:Envelope']['soap:Body']['ns2:PushResponse']['result']['status']
    if status == "92":
        return True
    else:
        return False


def checkMooveTransaction(transID):
    import requests,xmltodict,json
    # transID = "20086B3B-E229-4130-91BA-D0039405044D"
    # reqUrl = "https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/xml" 
    }

    payload = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="http://api.merchant.tlc.com/">
    \n <soapenv:Header/>
    \n <soapenv:Body>
    \n <api:getTransactionStatus>
    \n <token>5x6HzkGQz9cBfj6eO3n/rG0alcD8rIkXwWWBzl67LnwMhReWihY9SNcHXEX2H4r4</token>
    \n <request>
    \n <transid>'''+str(transID)+'''</transid>
    \n </request>
    \n </api:getTransactionStatus>
    \n </soapenv:Body>
    \n</soapenv:Envelope>'''

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList,verify=False)
    response_obj = xmltodict.parse(response.text)
    # response_json = json.loads(response_obj)
    status = response_obj['soap:Envelope']['soap:Body']['ns2:getTransactionStatusResponse']['response']['status']
    
    if status == "0":
        desc = response_obj['soap:Envelope']['soap:Body']['ns2:getTransactionStatusResponse']['response']['description']
        if desc == "SUCCESS":

            return True
    else:
        return False
    # return str(status)


def moove_main_call(amount,mobile):
    import uuid
    import time
    UUID_SMALL = str(uuid.uuid4())
    UUID_UPPER = UUID_SMALL.upper()

    # Check Moove User Existance

    msisdn_check = checkMSISDN(mobile)
    # time.sleep(10)
    if msisdn_check == True:
        # Go For Payment
        pay_request = sendPayRequest(MSISDN=mobile,UUID_UPPER=UUID_UPPER,AMOUNT=amount)
        time.sleep(30)
        check_request = checkMooveTransaction(UUID_UPPER)
        if check_request == True:
            return "SUCCESS"
        else:
            return "TRANSACTION FAILED"
    else:
        return "MOOVE USER NOT FOUND"