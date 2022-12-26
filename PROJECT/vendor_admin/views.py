from urllib import response
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
import random
import math
from django.core.mail import send_mail
from django.template.loader import render_to_string
from sqlalchemy import null
from eventinz_contact_details.models import EV_Contact
from eventmanager.models import event_entries, event_reviews_user_to_vendor, vendor_event_proposal, vendor_event_proposal_items
from transaction_records_user.models import Vendor_Payment_History, Vendor_Payment_History_events
from user_dashboard.models import user_login
from vendor_CMS.models import our_clients, our_clients_CMS, vendor_category_CMS, vendor_header, vendor_leads_CMS_main, vendor_leads_Steps, vendor_testimonials
from vendor_admin import models
from vendor_admin.models import Countries, States, Vendor_Users, Vendor_bank_listing, request_a_quote, total_accepted_orders, total_earnings, total_earnings_count, vendor_categories, vendor_filter_answers, vendor_gallery, vendor_leads_package, vendor_packages, vendor_public_deals, vendor_public_packages, vendor_question_type, vendor_questions, vendor_quote_invoice, vendor_sub_categories, vendor_subscription
from django.contrib import messages
from vendor_home.views import visitor_ip_address


from vendor_wallet.models import vendor_wallet_manager


from vendor_wallet.models import vendor_wallet_manager #import messages
def vendor_ip_address(request):

    if 'is_french' not in request.session:
        request.session['is_french']='No'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    import geoip2.database
    from pathlib import Path
    import os
    from django.http import JsonResponse

    BASE_DIR = Path(__file__).resolve().parent.parent
    l=os.path.join(BASE_DIR,'static/db/db.mmdb')
    reader = geoip2.database.Reader(l)

    response = reader.city(str(ip))
    data={}
    data['latitude']=str(response.location.latitude)
    data['longitude']=str(response.location.longitude)
    # print(response.location.latitude)
    # print(response.location.longitude)

    reader.close()
    from geopy.geocoders import Nominatim
 
# initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")
 
 
# Latitude & Longitude input
    Latitude = str(response.location.latitude)
    Longitude = str(response.location.longitude)
 
    location = geolocator.reverse(Latitude+","+Longitude)
 
    address = location.raw['address']
 
# traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    code = address.get('country_code')
    zipcode = address.get('postcode')
    if 'vendor_location_track' in request.session:
        pass
    else:

        request.session['vendor_location_track']=country
   
    if country == 'Bénin':
        country ='Benin'
        request.session['vendor_location_track']=country


    # request.session['user_country']=country
    # return HttpResponse(country)
    return request.session['vendor_location_track']

def check_vendor_profile(request):
    email = request.session['vendor_email']
    db = Vendor_Users.objects.get(Email = email)

    if db.profile_complete == False:
        return False
    else:
        return True

def check_vendor_bank(request):
    email = request.session['vendor_email']
    db = Vendor_Users.objects.get(Email = email).id
    vendor_bank=Vendor_bank_listing.objects.filter(Vendor_Id=db)
    bank_noti=False
    if vendor_bank.exists():
        bank_noti=False
    else:
        bank_noti=True
    return bank_noti
# def check_login_vendor(request):
    
def otp(request):
    email=request.session['vendor_email']
    request.session['email']=email
    fname=models.Vendor_Users.objects.get(Email=email).First_Name
    email_domain=email.split("@",1)[1]
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

## initializing a string
    random_str = ""

## we can generate any lenght of string we want
    for i in range(6):
## generating a random index
## if we multiply with 10 it will generate a number between 0 and 10 not including 10
## multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 10)

        random_str += str(digits[index])
    code_1=''
    count=1
    request.session['vendor_otp']=random_str
    ev_contact = EV_Contact.objects.get(id=1)
    content=render_to_string('vendor_admin1/otp_mail.html', {"fname":fname,"OTP":random_str,"ev_contact":ev_contact})
    send_mail(subject='Authenticate via OTP | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
    for i in email:
        if count<4:
            code_1+=i
            count+=1
        else:
            break
    context={
        
        "code_1":code_1,
        "domain":email_domain,
        "OTP":random_str,
        'is_french':request.session['is_french']

    }

    return render(request,'vendor_dashboard_v2/resend-otp.html',context)
# Create your views here.
def index(request):
    # if 'logged_in_vendor' not in request.session:
    #     return redirect('vendor_login')
       
    
    access=''
    
    if 'otp_verified' in request.session:
        otp_status=request.session['otp_verified']
        if otp_status == True :
            access=True
        elif otp_status == False:
            access = False
            # return redirect('vendor_auth')
            return redirect('verify_otp')
    elif 'vendor_email' not in request.session:
        return redirect('vendor_login')
    elif Vendor_Users.objects.get(Email=request.session['vendor_email']).is_otp_verified is True:
            access=True
    elif Vendor_Users.objects.get(Email=request.session['vendor_email']).is_otp_verified is False:
            access=False
            return redirect('verify_otp')


        
    
    if 'vendor_login' in request.session :
        vendor_login=request.session['vendor_login']
        request.session['email']=request.session['vendor_email']
        get_package=Vendor_Users.objects.get(Email=request.session['vendor_email']).package
        get_id=Vendor_Users.objects.get(Email=request.session['vendor_email']).id
        get_clicks=Vendor_Users.objects.get(Email=request.session['vendor_email']).profile_clicks

        if vendor_login==True:
            if get_package is None:
                return redirect('vendor_pricing')

            if not check_vendor_profile(request):
                messages.error(request,'Complete Your Profile , To Continue...')
                return redirect('vendor_profile_update')

            if check_vendor_bank(request):
                return redirect('my_bank')
            total_sales_count=0
            total_earning_count=0
            # total_sales=None
            try:
                total_sales=models.total_sales_count.objects.get(vendor_id=request.session['vendor_email'])
                total_sales_count=total_sales.total_count

            except models.total_sales_count.DoesNotExist:
                total_sales_count=0
                models.total_sales_count(vendor_id=request.session['vendor_email']).save()
            # if total_sales.exists():
            #     total_sales_count=total_sales.total_count
            try:
                total_earnings=models.total_earnings_count.objects.get(vendor_id=request.session['vendor_email'])
                total_earning_count=total_earnings.total_count
            except models.total_earnings_count.DoesNotExist:
                total_earning_count=0
            try:
                total_accepted_orders=models.total_accepted_orders.objects.get(vendor_id=get_id)
                total_accepted_orders_count=total_accepted_orders.order_count
            except models.total_accepted_orders.DoesNotExist:
                models.total_accepted_orders(vendor_id=get_id).save()
                total_accepted_orders_count=0
            
            try:
                total_orders=models.total_orders.objects.get(vendor_id=request.session['vendor_email'])
                total_orders_count=total_orders.order_count
            except models.total_orders.DoesNotExist:
                total_orders_count=0

            try:
                total_sales_graph=models.total_sales.objects.get(vendor_id=request.session['vendor_email'])    
            except models.total_sales.DoesNotExist:
                to=models.total_sales(vendor_id=request.session['vendor_email'])
                to.save()
                total_sales_graph=models.total_sales.objects.get(vendor_id=request.session['vendor_email'])

            get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
            get_country_currency=models.Countries.objects.get(name=get_user_country).currency
            from django.core.exceptions import ObjectDoesNotExist
            from datetime import date

            try:
                get_ev_leads=vendor_wallet_manager.objects.get(vendor_id=get_id)
            except ObjectDoesNotExist:
                vendor_wallet_manager(vendor_id=models.Vendor_Users.objects.get(Email=request.session['vendor_email']),total_balance='200',remaining_balance='200',last_recharged_on=str(date.today())).save()
                get_ev_leads=vendor_wallet_manager.objects.get(vendor_id=get_id)
            if (int(get_ev_leads.remaining_balance) <= 0 ):
                return redirect("renew_leads")
            get_u_data=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])
            get_vendor_id=get_u_data.id
            get_categories=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
            li = list(get_categories.split("__#__"))
            category_list_id=[]
            category_list=[]
            for i in li:
                if i == '':
                    break
                get_category_name=models.vendor_categories.objects.get(id=i).category_name
                category_list.append(get_category_name)
                category_list_id.append(i)

            # print(Convert(str1))
            search_query_events=get_categories.replace('__#__',',')
            event_posted=event_entries.objects.none()
            for i in category_list_id:
                curr_query = event_entries.objects.filter(vendor_type__icontains=str(i),status='draft')
                event_posted=event_posted|curr_query
            total_event_count=event_posted.count()
            vendor_pack=vendor_public_packages.objects.filter(vendor_id=request.session['vendor_email']).distinct('package_name').count()
            quote_req=request_a_quote.objects.filter(vendor_id=Vendor_Users.objects.get(id=get_vendor_id)).count()
            vendor_bank=Vendor_bank_listing.objects.filter(Vendor_Id=get_vendor_id)
            bank_noti=False
            if vendor_bank.exists():
                bank_noti=False
            else:
                bank_noti=True
            pending_approval=Vendor_Payment_History_events.objects.filter(vendor_id=get_vendor_id,status = "Pending Verification")
            quote_list = ['Transaction Pending for Verification']
            pending_approval_quote = request_a_quote.objects.filter(vendor_id=get_vendor_id,status__in=quote_list)
            from django.core import serializers

            get_categories=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
            li = list(get_categories.split("__#__"))
            category_list_id=[]
            category_list=[]
            for i in li:
                if i == '':
                    continue
                get_category_name=models.vendor_categories.objects.get(id=i).category_name
                category_list.append(get_category_name)
                category_list_id.append(i)

            # print(Convert(str1))
            search_query_events=get_categories.replace('__#__',',')
            event_posted=event_entries.objects.none()
            for i in category_list_id:
                curr_query = event_entries.objects.filter(vendor_type__icontains=str(i),status='draft')
                event_posted=event_posted|curr_query
            # event_posted_1=event_entries.objects.filter(vendor_type__icontains='20')

            # qs_json = serializers.serialize('json', event_posted.order_by('-created_on'))
            # return HttpResponse(qs_json, content_type='application/json')
            context={
                "currency":get_country_currency,
                'title':'Eventinz Vendor Dashboard',
                "total_earnings_count":total_earning_count,
                "total_sales_count":total_sales_count,
                "access":access,
                "total_accepted_orders_count":total_accepted_orders_count,
                "total_orders_count":total_orders_count,
                "monthly_data":total_sales_graph,
                "vendor_email":request.session['vendor_email'],
                'get_ev_leads':get_ev_leads,
                'u_data':get_u_data,
                'total_event_count':total_event_count,
                'get_clicks':get_clicks,
                'vendor_pack':vendor_pack,
                'quote_req':quote_req,
                'bank_noti':bank_noti,
                'is_french':request.session['is_french'],
                'pending_approval':pending_approval.count(),
                'pending_approval_quote':pending_approval_quote.count(),
                'ev':event_posted,
                'get_id':get_id,
                'ven_id':get_id,
                
            }
            return render(request,'vendor_dashboard_v2/index.html',context)
        else:
            return redirect('vendor_login')
    else:
        return redirect('vendor_login')

def login(request):
    if 'google_auto_login' in request.session:
        if request.session['google_auto_login']==True:
            request.session['vendor_email']=request.session['login_email']
            request.session['vendor_login']=True
            del request.session['login_email']
            del request.session['google_auto_login']
            return redirect('vendor_index')
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        # query=models.Vendor_Users.objects.get(Email=email)
        # if query.exists():
        query = ''

        try:
            query=Vendor_Users.objects.get(Email=email)
        except Vendor_Users.DoesNotExist:
            query = "NA"

        if(query == "NA"):
            messages.error(request,'Incorrect Email Credentials')
            return redirect('vendor_home')

        pass_check=query.Password
        if pass_check==password:
            request.session['vendor_login']=True
            request.session['vendor_email']=email
            return redirect('vendor_index')
        else:
            messages.error(request,'Incorrect Password Credentials')
            return redirect('vendor_index')
    return redirect('vendor_home')
    # return render(request,'vendor_admin1/pages-sign-in.html')
def signup(request):
    get_countries=Countries.objects.all().order_by('id')
    context={
        'countries':get_countries,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_admin2/vendor_registration.html',context)

def profile(request):
    if 'vendor_email' not in request.session:
        return redirect('vendor_login')
    get_package=Vendor_Users.objects.get(Email=request.session['vendor_email']).package
    context={
        "vendor_email":request.session['vendor_email'],
        'is_french':request.session['is_french']
    }
    if get_package is None:
        return redirect('vendor_pricing')
    else:
        user=Vendor_Users.objects.get(Email=request.session['vendor_email'])
        profile_img_stat=False
        if user.Profile_Img =='':
            profile_img_stat=False
        else:
            profile_img_stat=True
        # profile_img_stat=True
        if check_vendor_bank(request):
                return redirect('my_bank')
        get_categories=vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
        li = list(get_categories.split("__#__"))
        category_list=[]
        for i in li:
            if i == '':
                break

            get_category_name=vendor_categories.objects.get(id=i).category_name
            category_list.append(get_category_name)

        # print(Convert(str1))
        search_query_events=get_categories.replace('__#__',',')
        event_posted=event_entries.objects.none()
        for i in li:
            curr_query = event_entries.objects.filter(vendor_type__icontains=str(i))
            event_posted=event_posted|curr_query
        # event_posted=event_entries.objects.filter(vendor_type__icontains=search_query_events)
        ratings = event_reviews_user_to_vendor.objects.filter(vendor_id=user.id)
        
        vendor_bank = Vendor_bank_listing.objects.get(Vendor_Id=user.id)
        context={
            "user":user,
            "vendor_email":request.session['vendor_email'],
            "li":category_list,
            "pstat":profile_img_stat,
            'event_posted':event_posted,
            'is_french':request.session['is_french'],
            'ratings':ratings,
            'vendor_bank':vendor_bank,
            'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id
        }
    return render(request,'vendor_dashboard_v2/profile.html',context)

def profile_update(request):
    if 'vendor_email' not in request.session:
        return redirect('vendor_login')
    user=Vendor_Users.objects.get(Email=request.session['vendor_email'])
    get_categories=vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
    if user.Profile_Img =='':
        profile_img_stat=False
    else:
        profile_img_stat=True
    li = list(get_categories.split("__#__"))
    category_list=[]
    category_list_id=[]
    category_catering_name=[]
    category_catering_id=[]
    get_categories=vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
    li = list(get_categories.split("__#__"))
    li_int= []

    for i in li:
        if i == '':
            continue
        li_int.append(int(i))
    new_li=[]
    for j in li:
        if j == '':
            break
        new_li.append(j)
    category_list=[]
    for i in li:
        if i == '':
            continue
        get_category_name=vendor_categories.objects.get(id=i).category_name
        category_list.append(get_category_name)
    subcat_data=vendor_sub_categories.objects.filter(main_category__in=new_li)
    subcat_data_checked=user.vendor_sub_cat_data
    check_all=False
    check_data=''
    check_data_new=[]

    if subcat_data_checked == 'all':
        check_all=True
    else:
        check_all=False
        check_data=subcat_data_checked.split('__#__')
        for i in check_data:
            if i == '':
                
                break
            if i is None:
                break
            check_data_new.append(int(i))
    vendor_ques=vendor_questions.objects.filter(Question_Category__in=category_list_id)
    vendor_ques_cater=vendor_questions.objects.filter(Question_Category__in=category_catering_id)

    get_checked_items=user.question_field
    get_checked_catering=user.caterer_field
    get_checked_catering_values=get_checked_catering.keys()
    get_checked_items_values=get_checked_items.keys()
    get_checked_cater_list=[]
    get_checked_list=[]
    for x in get_checked_items_values:
        get_checked_list.append(x)
    for y in get_checked_catering_values:
        get_checked_cater_list.append(y)
    

    from django.core.exceptions import ObjectDoesNotExist
        # print(Convert(str1))
    
    ven_all_question=vendor_questions.objects.filter(Question_Category__in=new_li)
    try:
        qna=vendor_filter_answers.objects.filter(vendor_id=user)
    except ObjectDoesNotExist:
        qna='404'

    get_u_data=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])
    get_vendor_id=get_u_data.id

    context={
        "user":user,
        "vendor_email":request.session['vendor_email'],
        "li":category_list,
        "pstat":profile_img_stat,
        'v_ques':vendor_ques,
        'cater_ques':vendor_ques_cater,
        'get_checked_list':get_checked_list,
        'get_cater_checked_list':get_checked_cater_list,
        'sub_cat_data':subcat_data,
        'check_data':check_data_new,
        'check_all':check_all,
        'qna':qna,
        'vendor_questions':ven_all_question,
        'optgroup':li_int,
        'u_data':get_u_data,
        'is_french':request.session['is_french'],
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id
    }
    return render(request,'vendor_dashboard_v2/dashboard-edit-profile.html',context)
def pricing(request):
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/XOF'

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()
    
        # Your JSON object
        #1 USD = ... FCFA
    get_user_country=Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=Countries.objects.get(name=get_user_country).currency
    # ex_value=Exchange_Rates.objects.get(base_country='XOF',dest_country=get_country_currency).ex_rate
    # onefcfa=float(ex_value)

    # ex_value=Exchange_Rates.objects.get(base_country=get_currency_vendor,dest_country=get_user_currency).ex_rate


    import requests

    url = 'https://api.exchangerate.host/convert?from=XOF&to='+get_country_currency
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    # onefcfa=float(data['conversion_rates'][str(get_country_currency)])
    # amount=round(int(amount)*onefcfa)
    get_package=vendor_packages.objects.all()
    context={
                # "access":access,
                "vendor_email":request.session['vendor_email'],
                "packages":get_package,
                "conv_rate":onefcfa,
                "currency":get_country_currency,
                'is_french':request.session['is_french']
            }
    return render(request,'vendor_admin2/pricing.html',context)
def auth(request):
    import string
    fname=request.POST['fname']
    request.session['vendor_fname']=fname
    lname=request.POST['lname']
    company=request.POST['company']
    password=request.POST['password']
    re_password=request.POST['confirm_password']
    address=request.POST['company_address']
    country_code=request.POST['country']
    state_code=request.POST['state_val']
    phone=request.POST['phone']
    phone_code=request.POST['phone_code']
    al_phone=request.POST['al_phone']
    al_phone_code=request.POST['al_phone_code']
    Company_url=request.POST['Company_url']
    city = request.POST['vendor_city']
    User_ID=''.join(random.choices(string.ascii_uppercase +string.digits, k = 8))
    User_ID='EVTZV/'+User_ID
    get_country_name=Countries.objects.get(id=country_code).name
    request.session['user_selected_country']=get_country_name
    get_state_name=States.objects.get(state_code=state_code,country_name=get_country_name).name
    email=request.POST['email']
    query=Vendor_Users.objects.filter(Email=email)
    if query.exists():
        messages.error(request,"Email exists !!")
        return redirect('vendor_signup')
    if password!=re_password:
        messages.error(request,"Password Mismatch !")
        return redirect('vendor_signup')
    request.session['email']=email

    get_form=models.Vendor_Users(First_Name=fname,Last_Name=lname,phone_code=phone_code,Email=email,Company_Name=company,Password=password,country_code=country_code,state_code=state_code,country_name=get_country_name,state_name=get_state_name,User_ID=User_ID,Mobile=phone,Alternative_Mobile=al_phone,Company_Address=address,Company_url=Company_url,city_name=city)
    get_form.save()
    email_domain=email.split("@",1)[1]
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

## initializing a string
    random_str = ""

## we can generate any lenght of string we want
    for i in range(6):
## generating a random index
## if we multiply with 10 it will generate a number between 0 and 10 not including 10
## multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 10)

        random_str += str(digits[index])
    code_1=''
    count=1
    request.session['vendor_otp']=random_str
    ev_contact = EV_Contact.objects.get(id=1)
    content=render_to_string('vendor_admin1/otp_mail.html', {"fname":fname,"OTP":random_str,"ev_contact":ev_contact})
    send_mail(subject='Authenticate via OTP | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
    for i in email:
        if count<4:
            code_1+=i
            count+=1
        else:
            break
    context={
        "name":fname,
        "code_1":code_1,
        "domain":email_domain,
        "OTP":random_str,
        'is_french':request.session['is_french']

    }
    return render(request,'vendor_admin2/auth.html',context)

def auth_verify(request):
    if request.method=='POST':
        otp=request.POST['otp']
        if 'vendor_otp' in request.session:
            vendor_otp=request.session['vendor_otp']
            if otp==vendor_otp:
                del request.session['vendor_otp']
                request.session['otp_verified']=True
                get_form123=Vendor_Users.objects.get(Email=request.session['email'])
                get_form123.is_otp_verified=True
                get_form123.save()
                request.session['vendor_login']=True
                request.session['vendor_email']=request.session['email']
                return redirect('vendor_index')
            else:
                del request.session['vendor_otp']
                request.session['otp_verified']=False
                return redirect('vendor_auth')

def logout(request):
    request.session['vendor_login']=False
    del request.session['vendor_login']
    del request.session['vendor_email']
    return redirect('vendor_index')
def payment_session(request):
    request.session['amount']=request.GET['id']
    request.session['product_id']=request.GET['pid']
    request.session['oselect']=request.GET['oselect']
    return redirect('vendor_payment_page')
def payment(request):
    user_data=Vendor_Users.objects.get(Email=request.session['vendor_email'])
    product_data=vendor_packages.objects.get(id=request.session['product_id'])
    request.session['package_name']=product_data.package_name
    request.session['package_price']=request.session['amount']
    user_email=user_data.Email
    user_fname=user_data.First_Name
    user_lname=user_data.Last_Name
    user_company_name=user_data.Company_Name
    user_address=user_data.Company_Address
    user_username=user_data.User_ID
    user_city = user_data.city_name
    get_user_countryid=Vendor_Users.objects.get(Email=request.session['vendor_email']).country_code
    get_user_stateid=Vendor_Users.objects.get(Email=request.session['vendor_email']).state_code
    get_user_state=Vendor_Users.objects.get(Email=request.session['vendor_email']).state_name

    get_user_country=Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=Countries.objects.get(name=get_user_country).currency
    user_mobile=user_data.Mobile

    
    # currency_code=models.currency_model.objects.get(currency_code=get_country_currency)
    # currency_code_convert=currency_code.currency_code
    amount=0
    get_package=vendor_packages.objects.get(id=request.session['product_id']).is_enterprise_vendor
    package_type=request.session['oselect']
    if request.session['oselect']=='annual':
        amount=vendor_packages.objects.get(id=request.session['product_id']).price
    elif request.session['oselect']=='biannual':
        amount=vendor_packages.objects.get(id=request.session['product_id']).price_biannual
    elif request.session['oselect']=='quarter':
        amount=vendor_packages.objects.get(id=request.session['product_id']).price_quarter
    elif request.session['oselect']=='monthly':
        amount = vendor_packages.objects.get(id=request.session['product_id']).price_monthly
    
    # if currency_code_convert!='FCFA' or currency_code_convert!='CFA':
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/XOF'

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()

    #     # Your JSON object
    #     #1 USD = ... FCFA
    # onefcfa=float(data['conversion_rates'][str(get_country_currency)])
    # ex_value=Exchange_Rates.objects.get(base_country='XOF',dest_country=get_country_currency).ex_rate
    # onefcfa=float(ex_value)

    import requests

    url = 'https://api.exchangerate.host/convert?from=XOF&to='+get_country_currency
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    amount=round(int(amount)*onefcfa)
    get_categories=vendor_categories.objects.all()
        
    get_event_categories1=event_categories.objects.all()
    is_benin = False
    cntry = user_data.country_name
    # cntry = request.session['user_selected_country']
    if cntry == "Benin":
        is_benin = True
    
    context={
        "user_email":user_email,
        "vendor_email":user_email,
        "user_fname":user_fname,
        "user_lname":user_lname,
        "user_company_name":user_company_name,
        "user_address":user_address,
        'amount':amount,
        'product_data':product_data,
        'currency':get_country_currency,
        "userid":user_username,
        "country_code":get_user_countryid,
        "country_name":get_user_country,
        "state_code":get_user_stateid,
        "state_name":get_user_state,
        'mobile':user_mobile,
        "package_type":package_type,
        "get_package":get_package,
        "vendor_categories":get_categories,
        "get_event_cat":get_event_categories1,
        'user_city':user_city,
        'is_french':request.session['is_french'],
        'cntry':is_benin
    }
    return render(request,"vendor_admin2/payments.html",context)

def checkout_session(request,id):
    request.session['purchase_amount']=str(id)
    return redirect('Vendor_Checkout')

def checkout(request):
    if request.method=='GET':
        if request.GET['type']=='paypal':
            if request.GET['status']=='DONE':
                get_invoice_data=vendor_subscription.objects.get(invoice_id=request.session['invoice_id'])
                amt=request.GET.get('service_fee','')
                code=request.GET.get('code','')
                get_vendor_detail=Vendor_Users.objects.get(Email=request.session['vendor_email'])

                get_vendor_detail.package=request.session['package_name']
                get_vendor_detail.price=request.session['package_price']
                get_vendor_detail.save()
                if amt != '':
                    get_invoice_data.service_fee=float(amt)
                if code != '':

                    get_invoice_data.service_currency=code
                get_invoice_data.save()
                get_contact_details = EV_Contact.objects.get(id=1)

                context={
                "STATUS":'PAID',
                "TransID":request.GET['transid'],
                "amount":request.GET['amount'],
                "messages":'PAID',
                "inv_data":get_invoice_data,
                'is_french':request.session['is_french'],
                # "currency":country_cuurency
                'get_contact_details':get_contact_details

                }
                # content=render_to_string('vendor_admin1/invoice_mail.html', context)
                content=render_to_string('invoices/invoice-eventinz-1.html', context)

                send_mail(subject='Transaction Successfull ! | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)

                mail_data = {
                    'company_name':get_invoice_data.Vendor_company_name,
                    'get_contact_details':get_contact_details
                }
                content=render_to_string('Mail_Contents/Vendor_Welcome_Mail.html', mail_data)
                send_mail(subject='Welcome On Board !! - Eventinz Vendor | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
                # return render(request,'vendor_admin1/invoice.html',context)
                return redirect('vendor_index')

    amoun1t='100'
    # from datetime import datetime
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    import string
    import random
    if request.method=='POST':
        if request.POST['vendor_type']=='':
            messages.success(request,'Provide Valid Vendor Type and Continue')
            return redirect('vendor_checkout_session')
        amoun1t=request.POST['purchase_amount']
        # database12=vendor_subscription(package_name='Rownak')
        package_name=request.POST['package_name']
        package_description=request.POST['package_description']
        package_fee=request.POST['grand_total']
        package_category=request.POST.getlist('package_category')
        vendor_cat=request.POST.getlist('vendor_type')
        for i in package_category:

            get_category_name=event_categories.objects.get(id=i).category_name
            get_category_url=event_categories.objects.get(id=i).category_img
            vendor_id=request.session['vendor_email']
            event_category_serve=Vendor_Users.objects.get(Email=vendor_id).event_category_serve
            event_category_serve_json=event_category_serve
            question_category_serve=Vendor_Users.objects.get(Email=vendor_id).question_field
            question_category_serve_json=question_category_serve
            if i in event_category_serve_json:
                pass
            else:
                event_category_serve_json.update( {str(get_category_name) : 1} )

                Vendor_Users.objects.filter(Email=vendor_id).update(event_category_serve=event_category_serve_json)
            if i in question_category_serve:
                pass
            else:
                question_category_serve_json.update( {str(get_category_name) : str(get_category_url)})
                Vendor_Users.objects.filter(Email=vendor_id).update(question_field=question_category_serve_json)
            
        for i in vendor_cat:
            get_vendor_category_name=vendor_categories.objects.get(id=i).category_name
            get_vendor_json=Vendor_Users.objects.get(Email=vendor_id).vendor_categories
            get_vendor_json_update=get_vendor_json
            get_vendor_json_update.update({str(get_vendor_category_name) : 1})
            Vendor_Users.objects.filter(Email=vendor_id).update(vendor_categories=get_vendor_json_update)
        
                # service_fee=request.POST['service_fee']
        service_fee='0'
        
        payment_by=request.POST['paymentMethod1']
                # time=request.POST['time']
        time='1'
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        valid_from=datetime.today()
        up_months=0
        if request.session['oselect']=='annual':
            up_months=12
            # amount=models.vendor_packages.objects.get(id=request.session['product_id']).price
        elif request.session['oselect']=='biannual':
            up_months=6
            # amount=models.vendor_packages.objects.get(id=request.session['product_id']).price_biannual
        elif request.session['oselect']=='quarter':
            up_months=3
            # amount=models.vendor_packages.objects.get(id=request.session['product_id']).price_quarter
        valid_to = datetime.today()+ relativedelta(months=up_months)
        # print 'Today: ',datetime.today().strftime('%d/%m/%Y')
        # print 'After Month:', date_after_month.strftime('%d/%m/%Y')
                # invoice_date=datetime.date.today()

                # initializing size of string 
        N = 7
  
                # using random.choices()
                # generating random strings 
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N))
        invoice_id=''+str(res)
        request.session['invoice_id']=invoice_id

        vendor_name=request.POST['vendor_name']
        vendor_company_name=request.POST['vendor_company_name']
        vendor_phone=request.POST['vendor_phone']
        vendor_email=request.POST['vendor_email']
        purchase_type='Subscription Plan Purchase'
        vendor_type=request.POST['vendor_type_text']
        pre = "__#__"
        vendor_type = pre.join(vendor_cat) 


        # vendor_name='VendorName'
        # vendor_company_name='VendorDetails'
        # vendor_phone='phone'
        # vendor_email='email'
        # purchase_type='Subscription Plan Purchase'
        get_user_country=Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name

        country_cuurency=Countries.objects.get(name=get_user_country).currency

        database=vendor_subscription(valid_from=valid_from,valid_to=valid_to,package_name=package_name,package_description=package_description,package_fee=package_fee,service_fee='0',payment_by=payment_by,time=time,Vendor_name=vendor_name,Vendor_company_name=vendor_company_name,vendor_phone=vendor_phone,vendor_email=vendor_email,purchase_type=purchase_type,invoice_id=invoice_id,status='Pending',country_cuurency=country_cuurency,vendor_categories=vendor_type)

        database_vendor=Vendor_Users.objects.get(Email=request.session['vendor_email'])  
        database_vendor.package=package_name

        database_vendor.price=package_fee  
        database_vendor.event_categories=event_categories.objects.get(id=request.POST['event_category'])
                # database12.package_name='Rownak'
        database.save()
        # database_vendor.save

        if 'paymentMethod1' in request.POST:

            if request.POST['paymentMethod1']=='paypal':
                return render(request,'base/index_fresh.html',{"amount":amoun1t,'currency':country_cuurency})
            elif request.POST['paymentMethod1']=='moove':
                from vendor_home import moove_api
                number = request.POST['moove_number_input']
                payment = moove_api.moove_main_call(amount=str(amoun1t),mobile="229"+str(number))
            else:
                from vendor_home import momotran
                # data = momotran.main_call(str(amoun1t),str(vendor_phone),'EUR')

                number = request.POST['momo_number_input']
                payment = momotran.main_call_live(str(amoun1t),"229"+str(number),'XOF')
            import json

            if payment == False:
                return HttpResponse("Payment Status is False")
            elif payment == True or payment == "SUCCESS":
                from datetime import datetime
                from dateutil.relativedelta import relativedelta
                import string
                import random
                ivoice_id=invoice_id
                get_form123=vendor_subscription.objects.get(invoice_id=ivoice_id)
                get_form123.status='Paid'
                get_form123.save()
                get_vendor_detail=Vendor_Users.objects.get(Email=request.session['vendor_email'])
                get_vendor_detail.package=package_name
                get_vendor_detail.price=package_fee
                get_vendor_detail.save()
                get_invoice_data=vendor_subscription.objects.get(invoice_id=ivoice_id)
                from datetime import date
                vendor_wallet_manager(vendor_id=get_vendor_detail,total_balance='10',remaining_balance='10',last_recharged_on=str(date.today())).save()
                
                # get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name

                # country_cuurency=models.Countries.objects.get(name=get_user_country).currency
                get_contact_details = EV_Contact.objects.get(id=1)

                from django.core.cache import cache
                inv_data=cache.get('inv_data')
                if not inv_data:
                    inv_data = get_invoice_data
                    cache.set('inv_data',inv_data)

                context={
                # "STATUS":status['status'],
                # "TransID":status['financialTransactionId'],
                # "amount":status['amount'],
                # "messages":status['status'],
                "inv_data":get_invoice_data,
                'is_french':request.session['is_french'],
                'get_contact_details':get_contact_details
                # "currency":country_cuurency

                }
                content=render_to_string('invoices/invoice-eventinz-1.html', context)
                send_mail(subject='Transaction Successfull', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
                mail_data = {
                    'company_name':get_invoice_data.Vendor_company_name,
                    'get_contact_details':get_contact_details
                }
                content=render_to_string('Mail_Contents/Vendor_Welcome_Mail.html', mail_data)
                send_mail(subject='Welcome On Board !! - Eventinz Vendor | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
                # return render(request,'vendor_admin1/invoice.html',context)
                return redirect('vendor_index')

            else:
                return HttpResponse(payment)
            # context={
            #     "STATUS":status['status'],
            #     "TransID":status['financialTransactionId'],
            #     "amount":status['amount'],
            #     "messages":status['status']
            # }
            # if (status['status']=="SUCCESSFUL"):
                # conn.close()
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            import string
            import random
            ivoice_id=invoice_id
            get_form123=vendor_subscription.objects.get(invoice_id=ivoice_id)
            get_form123.status='Paid'
            get_form123.save()
            get_vendor_detail=Vendor_Users.objects.get(Email=request.session['vendor_email'])
            get_vendor_detail.package=package_name
            get_vendor_detail.price=package_fee
            get_vendor_detail.save()
            get_invoice_data=vendor_subscription.objects.get(invoice_id=ivoice_id)
            from datetime import date
            vendor_wallet_manager(vendor_id=get_vendor_detail,total_balance='200',remaining_balance='200',last_recharged_on=str(date.today())).save()
            
            # get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name

            # country_cuurency=models.Countries.objects.get(name=get_user_country).currency
            get_contact_details = EV_Contact.objects.get(id=1)

            from django.core.cache import cache
            inv_data=cache.get('inv_data')
            if not inv_data:
                inv_data = get_invoice_data
                cache.set('inv_data',inv_data)

            context={
            # "STATUS":status['status'],
            # "TransID":status['financialTransactionId'],
            # "amount":status['amount'],
            # "messages":status['status'],
            "inv_data":get_invoice_data,
            'is_french':request.session['is_french'],
            'get_contact_details':get_contact_details
            # "currency":country_cuurency

            }
            content=render_to_string('invoices/invoice-eventinz-1.html', context)
            send_mail(subject='Transaction Successfull', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
            mail_data = {
                'company_name':get_invoice_data.Vendor_company_name,
                'get_contact_details':get_contact_details
            }
            content=render_to_string('Mail_Contents/Vendor_Welcome_Mail.html', mail_data)
            send_mail(subject='Welcome On Board !! - Eventinz Vendor | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
            # return render(request,'vendor_admin1/invoice.html',context)
            return redirect('vendor_index')

        # else:
        #     return HttpResponse('MoMo Error')
            # return HttpResponse(str(data))
            # data_json = json.dumps(data,indent = 4)
            # json_obj = data_json
            
            # status = json.loads(json_obj)
            # return HttpResponse(status)

    # MoMO START

    #     import uuid
    #     uuidFour = uuid.uuid4()
    #     struuid=str(uuidFour)


    #     #print("UUID Generated")
    #     #print(struuid)

    #     ########### Python 3.2 #############
    #     import http.client, urllib.request, urllib.parse, urllib.error, base64

    #     headers = {
    #         # Request headers
    #         'X-Reference-Id': struuid,
    #         'Content-Type': 'application/json',
    #         'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    #     }

    #     params = urllib.parse.urlencode({
    #     })

    #     try:
    #         conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #         conn.request("POST", "/v1_0/apiuser?%s" % params, "{'providerCallbackHost': 'webhook.site'}", headers)
    #         #print("Request Sent")
    #         response = conn.getresponse()
    #         data = response.read()
    #         #print(data)
    #         #print("DATA RECIEVED")
    #         conn.close()
    #     except Exception as e:
    #         print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # ####################################
    #     ########### Python 3.2 #############
    # #print("CREATING HEADERS FOR GET USER")
    #     headers = {
    #         # Request headers
    #         'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    #     }
    # #print("HEADERS CREATED")
    #     params = urllib.parse.urlencode({
    #     })

    #     try:
    #         conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #         conn.request("GET", "/v1_0/apiuser/"+struuid+"?%s" % params, "{body}", headers)
    #         #print("REQUEST sent")
    #         response = conn.getresponse()
    #         data = response.read()
    #         #print(data)
    #         #print("DATA RECIEVED1")
    #         conn.close()
    #     except Exception as e:
    #         print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # ####################################

    #     import json
    #     headers = {
    #     # Request headers
    #         'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    #     }

    #     params = urllib.parse.urlencode({
    #     })

    #     try:
    #         conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #         conn.request("POST", "/v1_0/apiuser/"+struuid   +"/apikey?%s" % params, "{body}", headers)
    #         response = conn.getresponse()
    #         data = response.read()
    #         #print(data)
    #         x=json.loads(data)
        
        
    #         apikey=str(x['apiKey'])
            
    #         conn.close()
    #     except Exception as e:
    #         print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # ####################################
    #     import http.client, urllib.request, urllib.parse, urllib.error, base64
    #     sample_string = struuid+":"+apikey
    #     sample_string_bytes = sample_string.encode("ascii")
    
    #     base64_bytes = base64.b64encode(sample_string_bytes)
    #     base64_string = base64_bytes.decode("ascii")
    # #print(base64_string)
    #     headers = {
    #         # Request headers
    #         'Authorization': 'Basic '+base64_string,
    #         'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    #     }

    #     params = urllib.parse.urlencode({
    #     })

    #     try:
    #         conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #         conn.request("POST", "/collection/token/?%s" % params, "{body}", headers)
    #         response = conn.getresponse()
    #         data = response.read()
    #         #print(data)
    #         x=json.loads(data)
    #         accesstoken=x['access_token']
    #         #print("ACCESS START")
    #         #print(accesstoken)
    #         #print("ACCESS END")
    #         conn.close()
    #     except Exception as e:
    #         print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # ####################################
    # ########### Python 3.2 #############
    #     import http.client, urllib.request, urllib.parse, urllib.error, base64
    #     struuid1=str(uuid.uuid4())
    #     #sprint(struuid1)
    #     headers = {
    #         # Request headers
    #         'Authorization': 'Bearer '+accesstoken,
    #         'X-Callback-Url': 'https://webhook.site/eee2c577-71cf-47a7-8517-ed9b195bad58',
    #         'X-Reference-Id': struuid1,
    #         'X-Target-Environment': 'sandbox',
    #         'Content-Type': 'application/json',
    #         'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    #     }

    #     params = urllib.parse.urlencode({
    #     })

    #     amount=str(amoun1t)
    #     externalID='test'
    #     partyId='123456789'
    #     payerMessage='payermessage'
    #     payeeNote='payernote'
    #     body=str({"amount": amount,"currency": "EUR","externalId": externalID,"payer": {"partyIdType": "MSISDN","partyId": partyId},"payerMessage": payerMessage,"payeeNote": payeeNote})



    #     try:
    #         conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #         conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
    #         response = conn.getresponse()
    #         data = response.read()
    #         #print(data)
    #         conn.close()
    #     except Exception as e:
    #         print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # ####################################




    #     headers = {
    #         # Request headers
    #         'Authorization': 'Bearer '+accesstoken,
    #         'X-Target-Environment': 'sandbox',
    #         'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    #     }

    #     params = urllib.parse.urlencode({
    #     })

    #     try:
    #         conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #         conn.request("GET", "/collection/v1_0/requesttopay/"+struuid1+"?%s" % params, "{body}", headers)
    #         response = conn.getresponse()
    #         #print(response)
    #         data = response.read()
    #         #print(data)
    #         status=json.loads(data)
    #         #print(status['status'])
    #         context={
    #             "STATUS":status['status'],
    #             "TransID":status['financialTransactionId'],
    #             "amount":status['amount'],
    #             "messages":status['status']
    #         }
    #         if (status['status']=="SUCCESSFUL"):
    #             conn.close()
    #             from datetime import datetime
    #             from dateutil.relativedelta import relativedelta
    #             import string
    #             import random
    #             ivoice_id=invoice_id
    #             get_form123=vendor_subscription.objects.get(invoice_id=ivoice_id)
    #             get_form123.status='Paid'
    #             get_form123.save()
    #             get_vendor_detail=Vendor_Users.objects.get(Email=request.session['vendor_email'])
    #             get_vendor_detail.package=package_name
    #             get_vendor_detail.price=package_fee
    #             get_vendor_detail.save()
    #             get_invoice_data=vendor_subscription.objects.get(invoice_id=ivoice_id)
    #             from datetime import date
    #             vendor_wallet_manager(vendor_id=get_vendor_detail,total_balance='200',remaining_balance='200',last_recharged_on=str(date.today())).save()
                
    #             # get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name

    #             # country_cuurency=models.Countries.objects.get(name=get_user_country).currency
    #             get_contact_details = EV_Contact.objects.get(id=1)

    #             from django.core.cache import cache
    #             inv_data=cache.get('inv_data')
    #             if not inv_data:
    #                 inv_data = get_invoice_data
    #                 cache.set('inv_data',inv_data)

    #             context={
    #             "STATUS":status['status'],
    #             "TransID":status['financialTransactionId'],
    #             "amount":status['amount'],
    #             "messages":status['status'],
    #             "inv_data":get_invoice_data,
    #             'is_french':request.session['is_french'],
    #             'get_contact_details':get_contact_details
    #             # "currency":country_cuurency

    #         }
    #             content=render_to_string('vendor_admin1/invoice_mail.html', context)
    #             send_mail(subject='Transaction Successfull', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
    #             mail_data = {
    #                 'company_name':get_invoice_data.Vendor_company_name,
    #                 'get_contact_details':get_contact_details
    #             }
    #             content=render_to_string('Mail_Contents/Vendor_Welcome_Mail.html', mail_data)
    #             send_mail(subject='Welcome On Board !! - Eventinz Vendor | Eventinz - Your Event Your Way', message=mail_data, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=mail_data)
    #             return render(request,'vendor_admin1/invoice.html',context)

    #         else:
    #             if request.method=='GET':
    #                 if request.GET['type']=='paypal':
    #                     if request.GET['status']=='DONE':
    #                         get_invoice_data=vendor_subscription.objects.get(invoice_id=request.session['invoice_id'])
    #                         get_vendor_detail=Vendor_Users.objects.get(Email=request.session['vendor_email'])
    #                         get_vendor_detail.package=request.session['package_name']
    #                         get_vendor_detail.price=request.session['package_price']
    #                         get_vendor_detail.save()

    #                         context={
    #                         "STATUS":'PAID',
    #                         "TransID":request.GET['transid'],
    #                         "amount":request.GET['amount'],
    #                         "messages":'PAID',
    #                         "inv_data":get_invoice_data,
    #                         'is_french':request.session['is_french'],
    #                         'get_contact_details':get_contact_details
    #                         # "currency":country_cuurency

    #                         }
    #                         content=render_to_string('vendor_admin1/invoice_mail.html', context)
    #                         send_mail(subject='Transaction Successfull Updated', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
    #                         mail_data = {
    #                             'company_name':get_invoice_data.Vendor_company_name,
    #                             'get_contact_details':get_contact_details
    #                         }
    #                         content=render_to_string('Mail_Contents/Vendor_Welcome_Mail.html', mail_data)
    #                         send_mail(subject='Welcome On Board !! - Eventinz Vendor | Eventinz - Your Event Your Way', message=mail_data, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=mail_data)
    #                         return render(request,'vendor_admin1/invoice.html',context)
    #             return render(request,'vendor_admin1/success.html',context)
    #     except Exception as e:
    #         print("failed")
        
        
    

####################################


def payment_success(request):
    return render(request,'vendor_admin1/success.html')
def invoice(request):
    return render(request,'vendor_admin1/invoice.html')
    
def get_state(request):

    from django.http import HttpResponse
    from django.http import JsonResponse
    from django.core import serializers


    import json
    id=request.GET['id']
    qs = models.States.objects.filter(country_id=id)
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')

def get_email(request):
    
    from django.http import HttpResponse
    from django.http import JsonResponse
    from django.core import serializers


    import json
    id=request.GET['email']
    qs = models.Vendor_Users.objects.filter(Email=id)
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')

def google_auth_success(request):
    if request.user.is_authenticated:
        import string
        # user_id=request.user.id
        # # uid_auth=request.user.uid
        # extra_data=request.user.extra_data
        # email=extra_data.get('email')
        # provider=request.user.provider
        # if provider == 'google':
        first_name=request.user.first_name
        last_name=request.user.last_name
        password='no'
        Mobile=123
        Alternative_Mobile=1234
        is_otp_verified=True
        Company_Name='none'
        Company_Address='none'
        Company_url='none'
        country_code='none'
        state_code='none'
        country_name='Benin'
        state_name='none'
        User_ID=''.join(random.choices(string.ascii_uppercase +string.digits, k = 8))
        User_ID='EVTZV/'+User_ID
        email=request.user.email
        get_models_data=models.Vendor_Users.objects.filter(Email=email).count()
        if get_models_data >= 1:
            messages.info(request,"Email Exists ! Please Login to Continue")
            request.session['login_email']=email
            request.session['google_auto_login']=True
            return redirect('vendor_login')
        else:
            get_form=models.Vendor_Users(First_Name=first_name,Last_Name=last_name,Email=email,Company_Name=Company_Name,Password=password,country_code=country_code,state_code=state_code,country_name=country_name,state_name=state_name,User_ID=User_ID,Mobile=Mobile,Alternative_Mobile=Alternative_Mobile,Company_Address=Company_Address,Company_url=Company_url,is_otp_verified=is_otp_verified)
            get_form.save()
            request.session['vendor_email']=request.user.email
            request.session['otp_verified']=True
            request.session['vendor_login']=True
            return redirect('vendor_index')




# from somewhere import handle_uploaded_file

def vendor_update_profile(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        company=request.POST['company']
        password=request.POST['password']
        # re_password=request.POST['confirm_password']
        address=request.POST['company_address']
        # country_code=request.POST['country']
        # state_code=request.POST['state']
        phone=request.POST['mobile']
        # phone_code=request.POST['phone_code']
        al_phone=request.POST['al_mobile']
        # al_phone_code=request.POST['al_phone_code']
        Company_url=request.POST['Company_url']
        facebook_url=request.POST['facebook_url']
        instagram_url=request.POST['instagram_url']
        twitter_url=request.POST['twitter_url']
        linkedin_url=request.POST['linkedin_url']
        company_description=request.POST['company_about']
        min_budget=request.POST['min_budget']
        max_budget=request.POST['max_budget']
        vendor_new=request.POST.getlist('question_new')
        vendor_filter_answers.objects.filter(vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email'])).delete()
        for i in vendor_new:
            obj=vendor_questions.objects.get(id=int(i))
            vendor_filter_answers(question_id=obj,vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email']),answer_type=True).save()
        vendor_sub_cat_data=request.POST.getlist('ven_subs')

        sepa='__#__'
        sepa=sepa.join(vendor_sub_cat_data)
        get_json_feature=Vendor_Users.objects.get(Email=request.session['vendor_email']).question_field
        get_json_cater=Vendor_Users.objects.get(Email=request.session['vendor_email']).caterer_field
        feature_tags=request.POST.getlist('feature_tags')
        feature_tags_id=request.POST.getlist('feature_tags_id')
        feature_value=[]
        for j in feature_tags:
            for i in feature_tags_id:
                get_val_link=str(vendor_questions.objects.get(id=i).Question_Icon)
        # for i in feature_tags:
                feature_value.append(get_val_link)

        dict_z=''
      
        z=zip(feature_tags,feature_value)
        dict_z=dict(z)
        
        cater_tags=request.POST.getlist('cater_tags')
        cater_tags_id=request.POST.getlist('cater_tags_id')
        cater_value=[]
        for j in cater_tags:
            for i in cater_tags_id:
                get_val_link=str(vendor_questions.objects.get(id=i).Question_Icon)
        # for i in feature_tags:
                cater_value.append(get_val_link)

        dict_y=''
      
        y=zip(cater_tags,cater_value)
        dict_y=dict(y)
        # profile_img=request.FILES['file']
        if request.POST['fileval']=='YES':

        # handle_uploaded_file(request.FILES['file'])
            img_db=models.Vendor_Users.objects.get(id=request.POST['id'])

            img_db.Profile_Img=request.FILES['file']
            img_db.save(update_fields=['Profile_Img'])
        if password == '':

            models.Vendor_Users.objects.filter(id=request.POST['id']).update(First_Name=fname,Last_Name=lname,Company_Name=company,Company_Address=address,Mobile=phone,Alternative_Mobile=al_phone,Company_url=Company_url,facebook_url=facebook_url,instagram_url=instagram_url,twitter_url=twitter_url,linkedin_url=linkedin_url,Company_description=company_description,min_budget=min_budget,max_budget=max_budget,vendor_sub_cat_data=sepa,profile_complete=True)
        else:
             models.Vendor_Users.objects.filter(id=request.POST['id']).update(First_Name=fname,Last_Name=lname,Company_Name=company,Company_Address=address,Mobile=phone,Alternative_Mobile=al_phone,Company_url=Company_url,facebook_url=facebook_url,Password = password,instagram_url=instagram_url,twitter_url=twitter_url,linkedin_url=linkedin_url,Company_description=company_description,min_budget=min_budget,max_budget=max_budget,vendor_sub_cat_data=sepa,profile_complete=True)
        Vendor_Users.objects.filter(id=request.POST['id']).update(question_field=dict_z,caterer_field=dict_y)
        messages.info(request,'Profile Updated Successfully')
        return redirect('vendor_profile')

def test_google(request):
    return render(request,'vendor_admin1/test.html')

def my_deals_create(request):
    if 'vendor_email' not in request.session:
        return redirect('vendor_login')
    get_package=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).package
    context={
        "vendor_email":request.session['vendor_email'],
    }
    if get_package is None:
        return redirect('vendor_pricing')
    else:
        user=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])
        profile_img_stat=False
        if user.Profile_Img =='':
            profile_img_stat=False
        else:
            profile_img_stat=True
        # profile_img_stat=True
        get_categories=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
        li = list(get_categories.split("__#__"))
        category_list=[]
        for i in li:
            if i == '':
                break
            get_category_name=models.vendor_categories.objects.get(id=i).category_name
            category_list.append(get_category_name)

        packages=vendor_public_packages.objects.filter(vendor_id=request.session['vendor_email']).distinct('package_name')
        # print(Convert(str1))
        get_id=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).id
        get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
        get_country_currency=models.Countries.objects.get(name=get_user_country).currency
        context={
            "user":user,
            "vendor_email":request.session['vendor_email'],
            "li":category_list,
            "pstat":profile_img_stat,
            'packages':packages,
            "currency":get_country_currency,
            'is_french':request.session['is_french']
        }
    return render(request,'vendor_dashboard_v2/dashboard-create-deal.html',context)
def my_deals(request):
    if 'vendor_email' not in request.session:
        return redirect('vendor_login')
    
    get_package=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).package
    get_id=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).id
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    # context={
    #     "vendor_email":request.session['vendor_email'],
    #     "currency":get_country_currency
    # }
    if get_package is None:
        return redirect('vendor_pricing')
    else:
        user=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])
        if not check_vendor_profile(request):
            messages.error(request,'Complete Your Profile , To Continue...')
            return redirect('vendor_profile_update')

        if check_vendor_bank(request):
            return redirect('my_bank')
        profile_img_stat=False
        if user.Profile_Img =='':
            profile_img_stat=False
        else:
            profile_img_stat=True
        # profile_img_stat=True
        get_categories=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
        li = list(get_categories.split("__#__"))
        category_list=[]
        for i in li:
            if i == '':
                break
            get_category_name=models.vendor_categories.objects.get(id=i).category_name
            category_list.append(get_category_name)

        packages=vendor_public_packages.objects.filter(vendor_id=request.session['vendor_email']).distinct('package_name')

        deals_list=vendor_public_deals.objects.filter(vendor_id=get_id)
        # print(Convert(str1))
        context={
            "user":user,
            "vendor_email":request.session['vendor_email'],
            "li":category_list,
            "pstat":profile_img_stat,
            'packages':packages,
            "deals_list":deals_list,
            "currency":get_country_currency,
            'is_french':request.session['is_french']
        }
    return render(request,'vendor_dashboard_v2/dashboard-deals-page.html',context)
def my_deals_delete(request,id):
    db = vendor_public_deals.objects.get(id=id)
    db.delete()
    return redirect('vendor_my_deals')

from chat.models import Room

def my_chat(request,quote_id):
    user_email=request.session['vendor_email']
    get_user=Vendor_Users.objects.get(Email=user_email)
    # country=get_user.country
    # # get_country=Countries.objects.get(id=get_user.country).name
    # import requests

    # url = "https://api.countrystatecity.in/v1/countries/"+country

    # headers = {
    #     'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    # }

    # response = requests.request("GET", url, headers=headers)

    # print(response.text)
    import json
    import uuid
    id=quote_id
    get_req_quote_1=request_a_quote.objects.get(id=id)
    # data=json.loads(response.text)
    # get_country=data['name']
    user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
    user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
    username = get_req_quote_1.fname # henry
    username1=get_user.Company_Name
    room='EV-Rooms-'+str(username)

    room_details = Room.objects.get_or_create(name=room,quote_id=id)
    room_details = Room.objects.get(name=room,quote_id=id)

#     return render(request, 'room.html', {

    
# })

    context={
        'user':get_user,
        # 'country':get_country,
        'get_quotes':user_quote_req,
        "user_quote_req_count":user_quote_req_count,
        'room':room,
        'username': username,
    # 'room': room,
        'room_details': room_details,
        'quote_id':id,
        'username1':username1,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }

    # return render(request,'vendor_admin2/pages/chat.html',context)
    return render(request, 'vendor_dashboard_v2/dashboard_chat_popup.html',context)


def my_chat_events(request,quote_id):
    user_email=request.session['vendor_email']
    get_user=Vendor_Users.objects.get(Email=user_email)
    # country=get_user.country
    # # get_country=Countries.objects.get(id=get_user.country).name
    # import requests

    # url = "https://api.countrystatecity.in/v1/countries/"+country

    # headers = {
    #     'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    # }

    # response = requests.request("GET", url, headers=headers)

    # print(response.text)
    import json
    import uuid
    id=quote_id
    vendor_proposal = vendor_event_proposal.objects.get(id=id).event_id.id
    get_req_quote_1=event_entries.objects.get(id=vendor_proposal)
    # data=json.loads(response.text)
    # get_country=data['name']
    user_quote_req=event_entries.objects.filter(Email=user_email).order_by('-created_on')
    user_quote_req_count=event_entries.objects.filter(Email=user_email).count()
    username = get_req_quote_1.First_Name # henry
    username1=get_user.Company_Name
    room='EV-Rooms-Event'+str(username)

    room_details = Room.objects.get_or_create(name=room,quote_id=id)
    room_details = Room.objects.get(name=room,quote_id=id)

#     return render(request, 'room.html', {

    
# })

    context={
        'user':get_user,
        # 'country':get_country,
        'get_quotes':user_quote_req,
        "user_quote_req_count":user_quote_req_count,
        'room':room,
        'username': username,
    # 'room': room,
        'room_details': room_details,
        'quote_id':id,
        'username1':username1,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }

    # return render(request,'vendor_admin2/pages/chat.html',context)
    return render(request, 'vendor_dashboard_v2/dashboard-chat-event-popup.html',context)

def chatroom(request):
    return render(request,'vendor_admin2/pages/chatroom.html')

def chat_live(request):
    return render(request,'vendor_admin2/pages/chat_interface.html')

from content_app.models import Exchange_Rates, event_categories,event_categories_french,event_sub_categories,event_sub_categories_french

def my_packages(request):
    event_categorie=event_categories.objects.all()
    get_countries=models.Countries.objects.all().order_by('id')
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    context={
        'ev_cat':event_categorie,
        'countries':get_countries,
        'currency':get_country_currency,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/dashboard-create-a-package.html',context)

def my_packages_view(request):
    event_categorie=event_categories.objects.all()
    package_list=vendor_public_packages.objects.filter(vendor_id=request.session['vendor_email']).distinct('package_name')
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    context={
        'ev_cat':event_categorie,
        'package_list':package_list,
        'currency':get_country_currency,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/dashboard-packages-page.html',context)
def my_packages_view_single(request,name):
    event_categorie=event_categories.objects.all()
    package_list=vendor_public_packages.objects.filter(vendor_id=request.session['vendor_email'],package_name=name).distinct('package_name')
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    context={
        'ev_cat':event_categorie,
        'package_list':package_list,
        'currency':get_country_currency,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/dashboard-view-a-package.html',context)

def my_packages_edit(request,id):
    get_package=vendor_public_packages.objects.get(id=id)
    event_categorie=event_categories.objects.all()
    get_countries=models.Countries.objects.all().order_by('id')
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    context={
        'ev_cat':event_categorie,
        'countries':get_countries,
        "get_package":get_package,
        'currency':get_country_currency,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    # return render(request,'vendor_admin2/pages/my-package-edit.html',context)    
    return render(request,'vendor_dashboard_v2/dashboard-edit-a-package.html',context)    


def my_packages_on_post(request):
    if request.method=='POST':
        package_name=request.POST['package_name']
        what_included=request.POST['what_included']
        package_price=request.POST['package_price']
        package_category=request.POST['package_category']
        # get_cat_name=event_categories.objects.
        package_for=request.POST['package_for']
        valid_till=request.POST['valid_till']
        vendor_id=request.session['vendor_email']
        image=request.FILES['pthumbnail']
        sscountry=request.POST['scountry']
        sstate=request.POST.getlist('sstate')
        # attendee_range=request.POST['Attendees_range']
        at1=request.POST.get('Attendees_range_min','0')
        at2=request.POST.get('Attendees_range_max','0')

        attendee_range = str(at1) + '-' + str(at2)
        pricing_model=request.POST['pricing_model']
        max_price_range=request.POST['max_package_price']
        min_price_range=request.POST['min_package_price']
        get_category_name=event_categories.objects.get(id=package_category).category_name
        import json

        event_category_serve=models.Vendor_Users.objects.get(Email=vendor_id).event_category_serve
        event_category_serve_json=event_category_serve
        # return HttpResponse((event_category_serve))
        

        if package_category in event_category_serve_json:
            pass
        else:
            event_category_serve_json.update( {str(get_category_name) : 1} )
            models.Vendor_Users.objects.filter(Email=vendor_id).update(event_category_serve=event_category_serve_json)


        vendor_name=models.Vendor_Users.objects.get(Email=vendor_id).Company_Name
        for i in sstate:
            
            vendor_public_packages(package_name=package_name,pricing_model=pricing_model,what_included=what_included,attendee_range=attendee_range,package_price=package_price,package_category=package_category,package_for=package_for,valid_till=valid_till,vendor_id=vendor_id,category_name=get_category_name,location_country_code=sscountry,location_state_code=i,image=image,vendor_name=vendor_name,package_price_range_max=max_price_range,package_price_range_min=min_price_range).save()
        return redirect('my_packages_view')

def my_packages_edit_on_post(request):
    if request.method=='POST':
        id=request.POST['id']
        package_name=request.POST['package_name']
        what_included=request.POST['what_included']
        package_price=request.POST['package_price']
        package_category=request.POST['package_category']
        # get_cat_name=event_categories.objects.
        package_for=request.POST['package_for']
        valid_till=request.POST['valid_till']
        vendor_id=request.session['vendor_email']
        image=request.FILES.get('pthumbnail','')
        
        
        attendee_range=request.POST['Attendees_range']
        pricing_model=request.POST['pricing_model']

        get_category_name=event_categories.objects.get(id=package_category).category_name
        import json

        event_category_serve=models.Vendor_Users.objects.get(Email=vendor_id).event_category_serve
        event_category_serve_json=event_category_serve
        # return HttpResponse((event_category_serve))
        

        if package_category in event_category_serve_json:
            pass
        else:
            event_category_serve_json.update( {str(get_category_name) : 1} )
            models.Vendor_Users.objects.filter(Email=vendor_id).update(event_category_serve=event_category_serve_json)


        vendor_name=models.Vendor_Users.objects.get(Email=vendor_id).Company_Name
        # vendor_public_packages(package_name=package_name,pricing_model=pricing_model,what_included=what_included,attendee_range=attendee_range,package_price=package_price,package_category=package_category,package_for=package_for,valid_till=valid_till,vendor_id=vendor_id,category_name=get_category_name,location_country_code=sscountry,location_state_code=sstate,image=image,vendor_name=vendor_name).save()
        db = vendor_public_packages.objects.get(id=id)
        db.package_name=package_name
        db.what_included=what_included
        db.package_price=package_price
        db.pricing_model=pricing_model
        db.attendee_range=attendee_range
        db.package_category=package_category
        db.package_for=package_for
        db.valid_till=valid_till

        db.category_name=get_category_name
        if (image != ''):

            db.image=image
            db.save()
        else:
            db.save()

        return redirect('my_packages_view')

def my_packages_delete(request,id):
    db=vendor_public_packages.objects.get(id=id)
    title=db.package_name
    db_all=vendor_public_packages.objects.filter(package_name=title)
    db_all.delete()
    return redirect('my_packages_view')



def get_sub_categories(request):
    id=request.GET['id']
    sub_categories=event_sub_categories.objects.filter(category=id)
    from django.core import serializers
# serialize queryset
    sub_categories_json = serializers.serialize('json', sub_categories)
    return HttpResponse(sub_categories_json)

def my_listings(request):
    event_category=event_categories.objects.all()
    service_type=vendor_question_type.objects.all()
    context={
        'event_category':event_category,
        'service_type':service_type,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_admin2/pages/listings.html',context)

def my_gallery(request):
    if 'vendor_login' in request.session:
        if not check_vendor_profile(request):
            messages.error(request,'Complete Your Profile , To Continue...')
            return redirect('vendor_profile_update')

        if check_vendor_bank(request):
            return redirect('my_bank')
        event_category=event_categories.objects.all()
        service_type=vendor_question_type.objects.all()
        gallery=vendor_gallery.objects.filter(vendor_email=request.session['vendor_email'])
        context={
            'event_category':event_category,
            'service_type':service_type,
            "gallery":gallery,
            'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
            'is_french':request.session['is_french']
        }
        return render(request,'vendor_dashboard_v2/gallery.html',context)
    else:
        return redirect('vendor_index')
def my_gallery_create(request):
    event_category=event_categories.objects.all()
    service_type=vendor_question_type.objects.all()
    gallery=vendor_gallery.objects.filter(vendor_email=request.session['vendor_email'])
    context={
        'event_category':event_category,
        'service_type':service_type,
        "gallery":gallery,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/create-gallery.html',context)

def my_gallery_post(request):
    if request.method=='POST':
        photo_category=request.POST['photo_category']
        category_name=event_categories.objects.get(id=photo_category).category_name
        images=request.FILES.getlist('images')
        vendor_email=request.session['vendor_email']
        for image in images:
            photo=vendor_gallery.objects.create(photo_category=photo_category,category_name=category_name,photo_src=image,vendor_email=vendor_email)
        return redirect('my_gallery')
def my_gallery_delete(request,id):
    db=vendor_gallery.objects.get(id=id)
    db.delete()
    return redirect('my_gallery')




def my_quote_request(request):
    if 'vendor_login' in request.session:
        if not check_vendor_profile(request):
            messages.error(request,'Complete Your Profile , To Continue...')
            return redirect('vendor_profile_update')

        if check_vendor_bank(request):
            return redirect('my_bank')
        vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email']).id
        quotes=request_a_quote.objects.filter(vendor_id=vendor_id)
        context={
            'quotes':quotes,
            'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
            'is_french':request.session['is_french']
        }
        return render(request,'vendor_dashboard_v2/request-quote.html',context)
    else:
        return redirect('vendor_index')

def get_content(request):
    get_id=request.GET['id']
    quotes_msg=request_a_quote.objects.get(id=get_id).msg
    return HttpResponse(quotes_msg)



def quote_states(request):
    id=request.GET['id']
    ty=request.GET['type']
    if ty=='accept':
        vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email']).id

        get_lead=vendor_wallet_manager.objects.get(vendor_id=vendor_id)
        # if int(get_lead.remaining_balance) > 0 :
        #     from django.core.exceptions import ObjectDoesNotExist

        #     db=request_a_quote.objects.get(id=id)
        #     db.status='accept'
        #     db.save()
        #     get_lead.remaining_balance=str(int(get_lead.remaining_balance)-1)
        #     get_lead.save()
        #     get_total_order=total_accepted_orders.objects.get(vendor_id=vendor_id)
        #     get_total_order.order_count=get_total_order.order_count+1
        #     get_total_order.save()
        #     # todays_month = date.today().

        #     return HttpResponse("ok")
        
        if int(get_lead.remaining_balance) ==0:
            return HttpResponse("Insufficient Leads")
        else:
            return HttpResponse("ok")
    elif ty=='reject':
        db=request_a_quote.objects.get(id=id)
        db.status='reject'
        db.save()
        return HttpResponse("NOK")


def main_home(request):
    if 'vendor_email' in request.session:
        return redirect('vendor_index')
    vendor_cat=vendor_categories.objects.all()
    # vendor_header
    vendor_header_data=vendor_header.objects.get(id=1)
    vendor_leads_CMS_main_data=vendor_leads_CMS_main.objects.get(id=1)
    vendor_leads_steps_data=vendor_leads_Steps.objects.filter().order_by('step_no')
    vendor_category_CMS_data=vendor_category_CMS.objects.get(id=1)
    vendor_testi_data=vendor_testimonials.objects.get(id=1)
    vendor_clients_data=our_clients.objects.filter()
    vendor_clients_cms=our_clients_CMS.objects.get(id=1)

    context={
        'vendor_categories':vendor_cat,
        'vendor_testi_data':vendor_testi_data,
        'vendor_category_CMS_data':vendor_category_CMS_data,
        'vendor_leads_steps_data':vendor_leads_steps_data,
        'vendor_leads_CMS_main_data':vendor_leads_CMS_main_data,
        'vendor_header_data':vendor_header_data,
        'vendor_clients_data':vendor_clients_data,
        'vendor_clients_cms':vendor_clients_cms,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_admin2/vendor_pro.html',context)

def billing(request):
    import random
    quote_id=''
    for i in range(0,9):
        quote_id+=str(random.randint(1,9))
    vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email']).id

    quotation_for=request_a_quote.objects.filter(vendor_id=vendor_id,status='pending')
    import datetime
    from datetime import date
    start_date=str(date.today())
    date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    end_date = date_1 + datetime.timedelta(days=3)
    expire_at=end_date
    context={
        'quote_id':quote_id,
        'quotation_for':quotation_for,
        'expire_at':expire_at,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/creat-a-quote.html',context)

def get_quote_details(request):
    quote_id=request.GET['id']
    get_quote_db=request_a_quote.objects.get(id=quote_id)
    response_data={}
    response_data['id']=get_quote_db.id
    response_data['posted_on']=get_quote_db.created_on
    response_data['first_name']=get_quote_db.fname
    response_data['last_name']=get_quote_db.lname
    response_data['email']=get_quote_db.email
    response_data['phone']=get_quote_db.phone
    response_data['event_type']=get_quote_db.event_type
    response_data['appx_data']=get_quote_db.appx_date
    response_data['no_of_guests']=get_quote_db.no_of_guests
    response_data['msg']=get_quote_db.msg

    from django.http import JsonResponse
    return JsonResponse(response_data)


def bill_items(request):
    import html_to_json
    import json
    import requests
# import json
    link_data=''
    tax=request.GET['tax']
    data=request.GET['data']
    link_id=request.GET['link_id']
    id=request.GET['id']
    ptc=request.GET['ptc']
    quote_user=request.GET['quote_user']
    user_id=request.GET['user_id']
    e_date=request.GET['e_date']
    milestone=float(request.GET['milestone'])
    milestone_type=request.GET['milestone_type']
    final_amt=request.GET['final_amt']
    linkRequest = {
    "destination": "https://eventinz.com/staging/invoice/?quote_id="+id
    , "domain": { "fullName": "link.eventinz.com" }
    , "slashtag": str(id)
    , "title": "EV/"+str(id)
    }

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": "3a4f2d5bab6d4138810cd46a159dee15",
    
    }

    r = requests.post("https://api.rebrandly.com/v1/links/", 
        data = json.dumps(linkRequest),
        headers=requestHeaders)

    if (r.status_code == requests.codes.ok):
        link = r.json()
        # print(link)
        link_data=str(link["shortUrl"])
        # print("Long URL was %s, short URL is %s" % (link["destination"], link["shortUrl"]))

    
    html_string = str(data)
    tables = html_to_json.convert_tables(html_string)
    tables_json=tables[0]
    vendor_quote_invoice(vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email']),quote_id=id,link_id=link_id,quotation_items=tables_json,payment_terms=ptc,milestone=milestone,milestone_type=milestone_type,valid_till=e_date,short_link=link_data,total_amt=final_amt,quote_user=user_login.objects.get(Email=user_id),tax_percent=tax).save()
    db=request_a_quote.objects.get(id=quote_user)
    db.quote_id=vendor_quote_invoice.objects.get(quote_id=id)
    db.save()
    vendor_id=Vendor_Users.objects.get(Email=request.session['vendor_email']).id

    get_lead=vendor_wallet_manager.objects.get(vendor_id=vendor_id)
    if int(get_lead.remaining_balance) > 0 :
        from django.core.exceptions import ObjectDoesNotExist

        db=request_a_quote.objects.get(id=quote_user)
        db.status='accept'
        db.save()
        get_lead.remaining_balance=str(int(get_lead.remaining_balance)-1)
        get_lead.save()
        get_total_order=total_accepted_orders.objects.get(vendor_id=vendor_id)
        get_total_order.order_count=get_total_order.order_count+1
        get_total_order.save()
        # todays_month = date.today().

    #     return HttpResponse("ok")
    context={
        'tables':tables
    }
    return HttpResponse(link_data)
    # return render(request,'vendor_home/html.html',context)
def my_chat_dup(request):
    user_email=request.session['vendor_email']
    vendor_profile=Vendor_Users.objects.get(Email=user_email)
    reques=request_a_quote.objects.filter(vendor_id=vendor_profile)
    request1=vendor_event_proposal.objects.filter(vendor_id=vendor_profile)
    context={
        "reques":reques,
        'request1':request1,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/chat_view.html',context)

def request_rem_amt(request):
    id=request.GET['id']
    db=request_a_quote.objects.get(id=id)
    db.status='2nd Milestone requested'
    db.save()
    return HttpResponse("OK")


def vendor_send_otp(request):
    email=request.GET['email']
    request.session['fgt_email']=email
    
    fname=models.Vendor_Users.objects.get(Email=email).First_Name
    email_domain=email.split("@",1)[1]
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

## initializing a string
    random_str = ""

## we can generate any lenght of string we want
    for i in range(6):
## generating a random index
## if we multiply with 10 it will generate a number between 0 and 10 not including 10
## multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 10)

        random_str += str(digits[index])
    code_1=''
    count=1
    request.session['forgot_otp']=random_str
    content=render_to_string('vendor_admin1/otp_mail.html', {"fname":fname,"OTP":random_str})
    send_mail(subject='Reset Password | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
    for i in email:
        if count<4:
            code_1+=i
            count+=1
        else:
            break
    context={
        
        "code_1":code_1,
        "domain":email_domain,
        "OTP":random_str,
        'is_french':request.session['is_french']

    }
    return HttpResponse('DONE SENT')

def vendor_check_otp(request):
    sent_otp=request.session['forgot_otp']
    recieve_otp=request.GET['otp']
    if sent_otp == recieve_otp:
        return HttpResponse("OK")
    else:
        return HttpResponse("No")

def vendor_update_pwd(request):
    email=request.session['fgt_email']
    password=request.GET['password']

    db=Vendor_Users.objects.get(Email=email)
    db.Password=password
    db.save()
    return HttpResponse('Done')

def get_live_events(request):
    from django.core import serializers

    get_categories=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
    li = list(get_categories.split("__#__"))
    category_list_id=[]
    category_list=[]
    for i in li:
        if i == '':
            continue
        get_category_name=models.vendor_categories.objects.get(id=i).category_name
        category_list.append(get_category_name)
        category_list_id.append(i)

    # print(Convert(str1))
    search_query_events=get_categories.replace('__#__',',')
    event_posted=event_entries.objects.none()
    for i in category_list_id:
        curr_query = event_entries.objects.filter(vendor_type__icontains=str(i),status='draft')
        event_posted=event_posted|curr_query
    # event_posted_1=event_entries.objects.filter(vendor_type__icontains='20')

    qs_json = serializers.serialize('json', event_posted.order_by('-created_on'))
    return HttpResponse(qs_json, content_type='application/json')


def get_event_categories(request):
    id=request.GET['id']
    category_name=event_categories.objects.get(id=id).category_name
    return HttpResponse(category_name)
def get_vendor_categories(request):
    id=request.GET['id']
    category_name=vendor_categories.objects.get(id=id).category_name
    return HttpResponse(category_name)




def pricing_renewal(request):
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/XOF'

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()
    
        # Your JSON object
        #1 USD = ... FCFA
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    # ex_value=Exchange_Rates.objects.get(base_country='XOF',dest_country=get_country_currency).ex_rate
    # onefcfa=float(ex_value)

    import requests

    url = 'https://api.exchangerate.host/convert?from=XOF&to='+get_country_currency
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    # onefcfa=float(data['conversion_rates'][str(get_country_currency)])
    # amount=round(int(amount)*onefcfa)
    get_package=models.vendor_packages.objects.all()
    context={
                # "access":access,
                "vendor_email":request.session['vendor_email'],
                "packages":get_package,
                "conv_rate":onefcfa,
                "currency":get_country_currency,
                'is_french':request.session['is_french']
            }
    return render(request,'vendor_admin2/pricing_update.html',context)

def payment_session_update(request):
    request.session['amount']=request.GET['id']
    request.session['product_id']=request.GET['pid']
    request.session['oselect']=request.GET['oselect']
    return redirect('vendor_payment_renew')
def payment_renew(request):
    user_data=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])
    product_data=models.vendor_packages.objects.get(id=request.session['product_id'])
    user_event_categories=user_data.event_category_serve
    
    user_email=user_data.Email
    user_fname=user_data.First_Name
    user_lname=user_data.Last_Name
    user_company_name=user_data.Company_Name
    user_address=user_data.Company_Address
    user_username=user_data.User_ID
    get_user_countryid=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_code
    get_user_stateid=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).state_code
    get_user_state=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).state_name

    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    user_mobile=user_data.Mobile

    
    # currency_code=models.currency_model.objects.get(currency_code=get_country_currency)
    # currency_code_convert=currency_code.currency_code
    amount=0
    get_package=models.vendor_packages.objects.get(id=request.session['product_id']).is_enterprise_vendor
    package_type=request.session['oselect']
    if request.session['oselect']=='annual':
        amount=models.vendor_packages.objects.get(id=request.session['product_id']).price
    elif request.session['oselect']=='biannual':
        amount=models.vendor_packages.objects.get(id=request.session['product_id']).price_biannual
    elif request.session['oselect']=='quarter':
        amount=models.vendor_packages.objects.get(id=request.session['product_id']).price_quarter
    
    # if currency_code_convert!='FCFA' or currency_code_convert!='CFA':
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/XOF'

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()

    #     # Your JSON object
    #     #1 USD = ... FCFA
    # onefcfa=float(data['conversion_rates'][str(get_country_currency)])
    # ex_value=Exchange_Rates.objects.get(base_country='XOF',dest_country=get_country_currency).ex_rate
    # onefcfa=float(ex_value)

    import requests

    url = 'https://api.exchangerate.host/convert?from=XOF&to='+get_country_currency
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    amount=round(int(amount)*onefcfa)
    get_categories=models.vendor_categories.objects.all()
        
    get_event_categories1=models.event_categories.objects.all()
    get_categories_select=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
    li = list(get_categories_select.split("__#__"))
    category_list=[]
    for i in li:
        if i == '':
            break

        get_category_name=models.vendor_categories.objects.get(id=i).id
        category_list.append(get_category_name)
    
    context={
        "user_email":user_email,
        "vendor_email":user_email,
        "user_fname":user_fname,
        "user_lname":user_lname,
        "user_company_name":user_company_name,
        "user_address":user_address,
        'amount':amount,
        'product_data':product_data,
        'currency':get_country_currency,
        "userid":user_username,
        "country_code":get_user_countryid,
        "country_name":get_user_country,
        "state_code":get_user_stateid,
        "state_name":get_user_state,
        'mobile':user_mobile,
        "package_type":package_type,
        "get_package":get_package,
        "vendor_categories":get_categories,
        "get_event_cat":get_event_categories1,
        'li':category_list,
        'user_event_categories':user_event_categories,
        'is_french':request.session['is_french']
    }
    return render(request,"vendor_admin2/payments_renewal.html",context)



def active_events(request):
    from django.core import serializers

    get_categories=models.vendor_subscription.objects.get(vendor_email=request.session['vendor_email']).vendor_categories
    li = list(get_categories.split("__#__"))
    category_list_id=[]
    category_list=[]
    for i in li:
        if i == '':
            continue
        get_category_name=models.vendor_categories.objects.get(id=i).category_name
        category_list.append(get_category_name)
        category_list_id.append(i)

    # print(Convert(str1))
    search_query_events=get_categories.replace('__#__',',')
    event_posted=event_entries.objects.none()
    get_id=Vendor_Users.objects.get(Email=request.session['vendor_email']).id
    for i in category_list_id:
        curr_query = event_entries.objects.filter(vendor_type__icontains=str(i),status='draft')
        event_posted=event_posted|curr_query
    context = {
        'ev':event_posted,
        'get_id':get_id,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/Active_Events.html',context)

def checkout_session_renewal(request,id):
    request.session['purchase_amount']=str(id)
    return redirect('Vendor_Checkout_renewal')

def checkout_renewal(request):
    amoun1t='100'
    # from datetime import datetime
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    import string
    import random

    if request.method=='POST':
        if request.POST['vendor_type']=='':
            messages.success(request,'Provide Valid Vendor Type and Continue')
            return redirect('vendor_checkout_session')
        amoun1t=request.POST['purchase_amount']
        # database12=vendor_subscription(package_name='Rownak')
        package_name=request.POST['package_name']
        package_description=request.POST['package_description']
        package_fee=request.POST['grand_total']
        package_category=request.POST.getlist('package_category')
        vendor_cat=request.POST.getlist('vendor_type')
        vendor_id=request.session['vendor_email']

        for i in package_category:

            get_category_name=event_categories.objects.get(id=i).category_name
            get_category_url=event_categories.objects.get(id=i).category_img
            vendor_id=request.session['vendor_email']
            event_category_serve=models.Vendor_Users.objects.get(Email=vendor_id).event_category_serve
            event_category_serve_json=event_category_serve
            question_category_serve=models.Vendor_Users.objects.get(Email=vendor_id).question_field
            question_category_serve_json=question_category_serve
            if i in event_category_serve_json:
                pass
            else:
                event_category_serve_json.update( {str(get_category_name) : 1} )

                models.Vendor_Users.objects.filter(Email=vendor_id).update(event_category_serve=event_category_serve_json)
            if i in question_category_serve:
                pass
            else:
                question_category_serve_json.update( {str(get_category_name) : str(get_category_url)})
                models.Vendor_Users.objects.filter(Email=vendor_id).update(question_field=question_category_serve_json)
            
        for i in vendor_cat:
            get_vendor_category_name=models.vendor_categories.objects.get(id=i).category_name
            get_vendor_json=models.Vendor_Users.objects.get(Email=vendor_id).vendor_categories
            get_vendor_json_update=get_vendor_json
            get_vendor_json_update.update({str(get_vendor_category_name) : 1})
            models.Vendor_Users.objects.filter(Email=vendor_id).update(vendor_categories=get_vendor_json_update)
        
                # service_fee=request.POST['service_fee']
        service_fee='0'
                # payment_by=request.POST['payment_by']
        payment_by='Momo'
                # time=request.POST['time']
        time='1'
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        valid_from=datetime.today()
        up_months=0
        if request.session['oselect']=='annual':
            up_months=12
            # amount=models.vendor_packages.objects.get(id=request.session['product_id']).price
        elif request.session['oselect']=='biannual':
            up_months=6
            # amount=models.vendor_packages.objects.get(id=request.session['product_id']).price_biannual
        elif request.session['oselect']=='quarter':
            up_months=3
            # amount=models.vendor_packages.objects.get(id=request.session['product_id']).price_quarter
        valid_to = datetime.today()+ relativedelta(months=up_months)
        # print 'Today: ',datetime.today().strftime('%d/%m/%Y')
        # print 'After Month:', date_after_month.strftime('%d/%m/%Y')
                # invoice_date=datetime.date.today()

                # initializing size of string 
        N = 7
  
                # using random.choices()
                # generating random strings 
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N))
        invoice_id=''+str(res)
        vendor_name=request.POST['vendor_name']
        vendor_company_name=request.POST['vendor_company_name']
        vendor_phone=request.POST['vendor_phone']
        vendor_email=request.POST['vendor_email']
        purchase_type='Subscription Plan Purchase'
        vendor_type=request.POST['vendor_type_text']


        # vendor_name='VendorName'
        # vendor_company_name='VendorDetails'
        # vendor_phone='phone'
        # vendor_email='email'
        # purchase_type='Subscription Plan Purchase'
        get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name

        country_cuurency=models.Countries.objects.get(name=get_user_country).currency

        database=models.vendor_subscription.objects.get(vendor_email=vendor_email)

        # (valid_from=valid_from,valid_to=valid_to,package_name=package_name,package_description=package_description,package_fee=package_fee,service_fee='0',payment_by='momo',time=time,Vendor_name=vendor_name,Vendor_company_name=vendor_company_name,vendor_phone=vendor_phone,vendor_email=vendor_email,purchase_type=purchase_type,invoice_id=invoice_id,status='Pending',country_cuurency=country_cuurency,vendor_categories=vendor_type)
        database.valid_from=valid_from
        database.valid_to=valid_to
        database.payment_by=request.POST['paymentMethod1']
        database.package_name=package_name
        database.package_description=package_description
        database.package_fee=package_fee
        database.time=time
        database.Vendor_name=vendor_name
        database.Vendor_company_name=vendor_company_name
        database.vendor_phone=vendor_phone
        database.vendor_email=vendor_email
        database.purchase_type=purchase_type
        database.invoice_id=invoice_id
        database.vendor_categories=vendor_type
        database.country_cuurency=country_cuurency
        request.session['invoice_id']=invoice_id



        database_vendor=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])  
        database_vendor.package=package_name

        database_vendor.price=package_fee  
        database_vendor.event_categories=models.event_categories.objects.get(id=request.POST['event_category'])
                # database12.package_name='Rownak'
        database.save()
        # database_vendor.save

        if 'paymentMethod1' in request.POST:

            if request.POST['paymentMethod1']=='paypal':
                return render(request,'base/index.html',{"amount":amoun1t,'currency':country_cuurency})

    import uuid
    uuidFour = uuid.uuid4()
    struuid=str(uuidFour)


    #print("UUID Generated")
    #print(struuid)

    ########### Python 3.2 #############
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'X-Reference-Id': struuid,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/v1_0/apiuser?%s" % params, "{'providerCallbackHost': 'webhook.site'}", headers)
        #print("Request Sent")
        response = conn.getresponse()
        data = response.read()
        #print(data)
        #print("DATA RECIEVED")
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
    ########### Python 3.2 #############
#print("CREATING HEADERS FOR GET USER")
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    }
#print("HEADERS CREATED")
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("GET", "/v1_0/apiuser/"+struuid+"?%s" % params, "{body}", headers)
        #print("REQUEST sent")
        response = conn.getresponse()
        data = response.read()
        #print(data)
        #print("DATA RECIEVED1")
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################

    import json
    headers = {
    # Request headers
        'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/v1_0/apiuser/"+struuid   +"/apikey?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        x=json.loads(data)
        #print(x)
        #print("API START")
        apikey=str(x['apiKey'])
        #print(apikey)
        #print('api end')
        #print()
        #print(apikey)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    sample_string = struuid+":"+apikey
    sample_string_bytes = sample_string.encode("ascii")
  
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
#print(base64_string)
    headers = {
        # Request headers
        'Authorization': 'Basic '+base64_string,
        'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
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
        accesstoken=x['access_token']
        #print("ACCESS START")
        #print(accesstoken)
        #print("ACCESS END")
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
########### Python 3.2 #############
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    struuid1=str(uuid.uuid4())
    #sprint(struuid1)
    headers = {
        # Request headers
        'Authorization': 'Bearer '+accesstoken,
        'X-Callback-Url': 'https://webhook.site/eee2c577-71cf-47a7-8517-ed9b195bad58',
        'X-Reference-Id': struuid1,
        'X-Target-Environment': 'sandbox',
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    }

    params = urllib.parse.urlencode({
    })

    amount=str(amoun1t)
    externalID='test'
    partyId='123456789'
    payerMessage='payermessage'
    payeeNote='payernote'
    body=str({"amount": amount,"currency": "EUR","externalId": externalID,"payer": {"partyIdType": "MSISDN","partyId": partyId},"payerMessage": payerMessage,"payeeNote": payeeNote})



    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################




    headers = {
        # Request headers
        'Authorization': 'Bearer '+accesstoken,
        'X-Target-Environment': 'sandbox',
        'Ocp-Apim-Subscription-Key': 'e2d5f82d308c412dae7d5436d6a52ac0',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
        conn.request("GET", "/collection/v1_0/requesttopay/"+struuid1+"?%s" % params, "{body}", headers)
        response = conn.getresponse()
        #print(response)
        data = response.read()
        #print(data)
        status=json.loads(data)
        #print(status['status'])
        context={
            "STATUS":status['status'],
            "TransID":status['financialTransactionId'],
            "amount":status['amount'],
            "messages":status['status'],
            'is_french':request.session['is_french']
        }
        if (status['status']=="SUCCESSFUL"):
            conn.close()
            from datetime import datetime
            from dateutil.relativedelta import relativedelta
            import string
            import random
            ivoice_id=invoice_id
            get_form123=models.vendor_subscription.objects.get(invoice_id=ivoice_id)
            get_form123.status='Paid'
            get_form123.save()
            get_vendor_detail=models.Vendor_Users.objects.get(Email=request.session['vendor_email'])
            get_vendor_detail.package=package_name
            get_vendor_detail.price=package_fee
            get_vendor_detail.save()
            get_invoice_data=models.vendor_subscription.objects.get(invoice_id=ivoice_id)
            from datetime import date
           
            
            # get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name

            # country_cuurency=models.Countries.objects.get(name=get_user_country).currency
            
            # request.session['inv_data']=get_invoice_data
            from django.core.cache import cache
            inv_data=cache.get('inv_data')
            if not inv_data:
                inv_data = get_invoice_data
                cache.set('inv_data',inv_data)

            context={
            "STATUS":status['status'],
            "TransID":status['financialTransactionId'],
            "amount":status['amount'],
            "messages":status['status'],
            "inv_data":get_invoice_data,
            'is_french':request.session['is_french']
            # "currency":country_cuurency

        }
            content=render_to_string('vendor_admin1/invoice_mail.html', context)
            send_mail(subject='Transaction Successfull Updated', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
            return render(request,'vendor_admin1/invoice.html',context)

        else:
            if request.method=='GET':
                if request.GET['type']=='paypal':
                    if request.GET['status']=='DONE':
                        get_invoice_data=models.vendor_subscription.objects.get(invoice_id=request.session['invoice_id'])

                        context={
                        "STATUS":'PAID',
                        "TransID":request.GET['transid'],
                        "amount":request.GET['amount'],
                        "messages":'PAID',
                        "inv_data":get_invoice_data,
                        # "currency":country_cuurency
                        'is_french':request.session['is_french']

                        }
                        content=render_to_string('vendor_admin1/invoice_mail.html', context)
                        send_mail(subject='Transaction Successfull Updated', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
                        return render(request,'vendor_admin1/invoice.html',context)
            return render(request,'vendor_admin1/success.html',context)
    except Exception as e:
        print("failed")
    
    
    if request.method=='GET':
        if request.GET['type']=='paypal':
            if request.GET['status']=='DONE':
                get_invoice_data=models.vendor_subscription.objects.get(invoice_id=request.session['invoice_id'])
                amt=request.GET.get('service_fee','')
                


                code=request.GET.get('code')
                if amt != '':
                    get_invoice_data.service_fee=float(amt)
                if code != '' or code == None:

                    get_invoice_data.service_currency=code
                get_invoice_data.save()
                context={
                "STATUS":'PAID',
                "TransID":request.GET['transid'],
                "amount":request.GET['amount'],
                "messages":'PAID',
                "inv_data":get_invoice_data,
                'is_french':request.session['is_french']
                # "currency":country_cuurency

                }
                content=render_to_string('vendor_admin1/invoice_mail.html', context)
                send_mail(subject='Transaction Successfull Updated', message=content, from_email='support@eventinz.com', recipient_list=[request.session['vendor_email']], html_message=content)
                return render(request,'vendor_admin1/invoice.html',context)

def save_deals(request):
    package_id=request.POST['package_name']
    deal_name=request.POST['deal_name']
    package_object=vendor_public_packages.objects.get(id=package_id)
    deal_price=request.POST['deal_price']
    deal_by=request.POST['deal_by']
    vendor_id=request.session['vendor_email']
    user_obj=Vendor_Users.objects.get(Email=vendor_id)
    vendor_public_deals(package_name=package_object,deal_price=deal_price,deal_by=deal_by,deal_name=deal_name,vendor_id=user_obj).save()
    return redirect('vendor_my_deals')

def event_live(request):
    return HttpResponse("OK")

def event_live_details(request,id):
    
    user=request.session['vendor_email']
    user_obj=Vendor_Users.objects.get(Email=user)
    event_data=event_entries.objects.get(id=int(id))
    check_proposal = vendor_event_proposal.objects.filter(vendor_id=user_obj.id,event_id=id)
    check_proposal_valid=False
    check_leads = vendor_wallet_manager.objects.get(vendor_id=user_obj.id).remaining_balance
    if (int(check_leads) <= 0):
        return redirect("renew_leads")

    if check_proposal.exists():
        check_proposal_valid = False
    else:
        check_proposal_valid = True
    context={
        'event_data':event_data,
        'location': user_obj.country_name,
        'event_id':id,
        'check_proposal_valid':check_proposal_valid,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'get_user_location':vendor_ip_address(request),
        'is_french':request.session['is_french']
        

    }
    return render(request,'vendor_dashboard_v2/create-proposal.html',context)
def event_live_details_edit(request,id,proposal_id):
    
    user=request.session['vendor_email']
    user_obj=Vendor_Users.objects.get(Email=user)
    event_data=event_entries.objects.get(id=int(id))
    check_proposal = vendor_event_proposal.objects.filter(vendor_id=user_obj.id,event_id=id)

    check_proposal_valid=False
    db=''
    proposal_items=''
    if check_proposal.exists():
        check_proposal_valid = True
        db=vendor_event_proposal.objects.get(vendor_id = user_obj.id,event_id=id,id=proposal_id)
        proposal_items=vendor_event_proposal_items.objects.filter(proposal_id=db.id)
    else:
        check_proposal_valid = False
    context={
        'event_data':event_data,
        'location': user_obj.country_name,
        'event_id':id,
        'check_proposal_valid':check_proposal_valid,
        'db':db,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'proposal_items':proposal_items,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/create-proposal-edit.html',context)

def save_event_proposal(request):
    vendor_id=request.session['vendor_email']
    user_obj=Vendor_Users.objects.get(Email=vendor_id)
    event_id=request.POST['event_id']
    event_id_obj=event_entries.objects.get(id=event_id)
    cover_letter=request.POST['cover_letter']
    state_tax=request.POST['state_tax']
    grand_total=request.POST['gtotal']
    total=request.POST.getlist('total')
    total_sum=0.00
    for i in total:
        total_sum+=float(i)
    vendor_event_proposal(vendor_id=user_obj,event_id=event_id_obj,cover_letter=cover_letter,total_amount=total_sum,state_tax=state_tax,grand_total=grand_total).save()
    # total_amount=request.POST['total_amount']
    get_id=vendor_event_proposal.objects.get(vendor_id=user_obj.id,event_id=event_id_obj.id,cover_letter=cover_letter,total_amount=total_sum).id
    get_vendor_id=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).id
   
    get_ev_leads=vendor_wallet_manager.objects.get(vendor_id=get_vendor_id)
    bal=int(get_ev_leads.remaining_balance)
    bal-=1
    bal=str(bal)
    get_ev_leads.remaining_balance=bal
    get_ev_leads.save()
    item=request.POST.getlist('description')
    qty=request.POST.getlist('qty')
    unit=request.POST.getlist('unit')
    rate=request.POST.getlist('rate')
    get_total_item=len(item)
    for i in range(0,get_total_item):
        item_single=item[i]
        qty_single=qty[i]
        unit_single=unit[i]
        rate_single=rate[i]
        total_single=total[i]
        vendor_event_proposal_items(proposal_id=vendor_event_proposal.objects.get(id=get_id),item=item_single,qty=qty_single,unit=unit_single,rate=rate_single,total=total_single).save()
    mail_data={
        'fname':event_id_obj.First_Name,
        'lname':event_id_obj.Last_Name,
        'vendor_company':user_obj.Company_Name,
        'event_type':event_id_obj.Event_Categories
    }
    content=render_to_string('Mail_Contents/proposal_recieved_event.html', mail_data)
    send_mail(subject='Proposal Recieved ! | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[event_id_obj.Email], html_message=content) 
    return redirect('vendor_index')
def save_event_proposal_update(request):
    vendor_id=request.session['vendor_email']
    user_obj=Vendor_Users.objects.get(Email=vendor_id)
    event_id=request.POST['event_id']
    event_id_obj=event_entries.objects.get(id=event_id)
    cover_letter=request.POST['cover_letter']
    state_tax=request.POST['state_tax']
    grand_total=request.POST['gtotal']
    total=request.POST.getlist('total')
    total_sum=0.00
    for i in total:
        total_sum+=float(i)

    get_id=vendor_event_proposal.objects.get(vendor_id=user_obj.id,event_id=event_id_obj.id).id
    db_proposal = vendor_event_proposal.objects.get(id=get_id)
    db_proposal.cover_letter = cover_letter
    db_proposal.total_amount = total_sum
    db_proposal.state_tax = state_tax
    db_proposal.grand_total = grand_total
    db_proposal.total_amount = total_sum
    db_proposal.save()

    item=request.POST.getlist('description')
    qty=request.POST.getlist('qty')
    unit=request.POST.getlist('unit')
    rate=request.POST.getlist('rate')
    get_total_item=len(item)
    vendor_event_proposal_items.objects.filter(proposal_id=get_id).delete()
    for i in range(0,get_total_item):
        item_single=item[i]
        qty_single=qty[i]
        unit_single=unit[i]
        rate_single=rate[i]
        total_single=total[i]
        vendor_event_proposal_items(proposal_id=vendor_event_proposal.objects.get(id=get_id),item=item_single,qty=qty_single,unit=unit_single,rate=rate_single,total=total_single).save()
    mail_data={
        'fname':event_id_obj.First_Name,
        'lname':event_id_obj.Last_Name,
        'vendor_company':user_obj.Company_Name,
        'event_type':event_id_obj.Event_Categories
    }
    content=render_to_string('Mail_Contents/proposal_recieved_event.html', mail_data)
    send_mail(subject='Proposal Updated ! | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[event_id_obj.Email], html_message=content) 
    return redirect('vendor_index')
def event_transactions(request):
    vendor_email = request.session['vendor_email']
    vendor_id=Vendor_Users.objects.get(Email=vendor_email).id
    db = Vendor_Payment_History_events.objects.filter(vendor_id=vendor_id).order_by('-created_at')
    vendor_bank=Vendor_bank_listing.objects.filter(Vendor_Id=vendor_id)
    bank_noti=False
    if vendor_bank.exists():
        bank_noti=False
    else:
        bank_noti=True
    context={
        "records":db,
        'bank_noti':bank_noti,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/event_transac.html',context)

def proposal_transactions(request):
    vendor_email = request.session['vendor_email']
    vendor_id=Vendor_Users.objects.get(Email=vendor_email).id
    db = request_a_quote.objects.filter(vendor_id=vendor_id,status__in=['Transaction Pending for Verification','2nd Milestone requested','Milestone Paid','2nd Milestone Paid']).order_by('-created_on')
    vendor_bank=Vendor_bank_listing.objects.filter(Vendor_Id=vendor_id)
    bank_noti=False
    if vendor_bank.exists():
        bank_noti=False
    else:
        bank_noti=True
    context={
        "records":db,
        'bank_noti':bank_noti,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/proposal-payments.html',context)

def my_proposals(request):
    vendor_email = request.session['vendor_email']
    vendor_id=Vendor_Users.objects.get(Email=vendor_email).id
    proposal = vendor_event_proposal.objects.filter(vendor_id=vendor_id).order_by('-created_on')
    context = {
        "proposal":proposal,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/my_proposals.html',context)

def my_bank(request):
    vendor_email = request.session['vendor_email']
    vendor_id=Vendor_Users.objects.get(Email=vendor_email).id
    vendor_bank=Vendor_bank_listing.objects.filter(Vendor_Id=vendor_id)
    bank_noti=False
    if vendor_bank.exists():
        bank_noti=True
    else:
        bank_noti=False
    
    context={
        "bank_noti":bank_noti,
        'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
        'is_french':request.session['is_french']
    }

    return render(request,'vendor_dashboard_v2/bank_details.html',context)


def my_bank_add(request):
    vendor_email = request.session['vendor_email']
    vendor_id=Vendor_Users.objects.get(Email=vendor_email)
    Bank_Name=request.POST.get('Bank_Name')
    Account_Name=request.POST.get('Account_Name')
    Bank_Account_Number=request.POST.get('Bank_Account_Number')
    Country=request.POST.get('Country')
    Code_Banque=request.POST.get('Code_Banque')
    Code_Guichet=request.POST.get('Code_Guichet')
    Cle_RIB=request.POST.get('Cle_RIB')
    IBAN=request.POST.get('IBAN')
    Code_Swift=request.POST.get('Code_Swift')
    Domiciliation=request.POST.get('Domiciliation')
    PayPal_Account_Name=request.POST.get('PayPal_Account_Name')
    Paypal_ID=request.POST.get('Paypal_ID')
    MoMo_Number=request.POST.get('MoMo_Number')


    is_bank = False
    is_paypal = False
    is_momo = False

    if(PayPal_Account_Name == '' or Paypal_ID == ''):
        is_paypal = False
    else:
        is_paypal = True
    if(MoMo_Number == ''):
        is_momo = False
    else:
        is_momo = True
    if(Bank_Name == '' or Account_Name == '' or Bank_Account_Number == '' or Country == '' or Code_Banque == '' or Code_Guichet == '' or Cle_RIB == '' or IBAN == '' or Code_Swift == '' or Domiciliation == ''):
        is_bank = False
    else:
        is_bank = True
    url = request.POST['url']
    if (is_bank == False and is_momo == False and is_paypal == False):
        return redirect('vendor_index')
    else:

        Vendor_bank_listing(Vendor_Id=vendor_id,Bank_Name=Bank_Name,Account_Name=Account_Name,Bank_Account_Number=Bank_Account_Number,Country=Country,Code_Banque=Code_Banque,Code_Guichet=Code_Guichet,Cle_RIB=Cle_RIB,IBAN=IBAN,Code_Swift=Code_Swift,Domiciliation=Domiciliation,PayPal_Account_Name=PayPal_Account_Name,Paypal_ID=Paypal_ID,MoMo_Number=MoMo_Number,is_paypal=is_paypal,is_bank=is_bank,is_momo=is_momo).save()

        return redirect('vendor_index')

def accept_trans(request,id):
    db = Vendor_Payment_History_events.objects.get(id=id)
    db.status = 'Paid'
    amount = db.Amount
    amount_final = 0
    curr = 'XOF'
    Bank_Name = db.Bank_Name
    if Bank_Name == 'PayPal':
        curr = 'USD'
    if curr == 'USD' :
        import requests

        url = 'https://api.exchangerate.host/convert?from=USD&to='+curr
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['info']['rate'])
        
        amount_final=round(onefcfa*float(amount),2)
    if curr == 'XOF':
        amount_final=amount
    
    db.save()
    return redirect('event_transactions')

def reject_trans(request,id):
    db = Vendor_Payment_History_events.objects.get(id=id)
    db.status = 'Rejected'
    db.save()
    return redirect('event_transactions')

def renew_leads(request):
    get_leads_package = vendor_leads_package.objects.all()
    is_benin = False
    cntry = request.session['user_location_track']
    if cntry == "Benin":
        is_benin = True
    vendor_momo = Vendor_bank_listing.objects.get(Vendor_Id=Vendor_Users.objects.get(Email=request.session['vendor_email'])).is_momo
    
    context = {
       'leads_package':get_leads_package ,
       'ven_id': Vendor_Users.objects.get(Email=request.session['vendor_email']).id,
       'cntry':is_benin,
       'vendor_momo':vendor_momo,
       'is_french':request.session['is_french']
    }
    return render(request,'vendor_dashboard_v2/renew-leads.html',context)

from vendor_home import momotran
def renew_leads_momo(request):
    amount = request.GET['amount']
    lead_type = request.GET['type']
    vendor_id = Vendor_Users.objects.get(Email=request.session['vendor_email'])
    mobile = Vendor_Users.objects.get(Email=request.session['vendor_email']).Mobile
    # momo_mobile = "229"+str(Vendor_bank_listing.objects.get(Vendor_Id=vendor_id.id).MoMo_Number)
    momo_mobile = request.GET['number']
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    currency = get_country_currency

    # momotran.main_call(amount,mobile,currency)
    payment = momotran.main_call_live(str(amount),str(momo_mobile),'XOF')

    if payment == False:
        return HttpResponse("Error")
    elif payment == True:
        
        get_user = Vendor_Users.objects.get(Email = request.session['vendor_email'])
        get_wallet = vendor_wallet_manager.objects.get(vendor_id=get_user.id)
        get_package_count = vendor_leads_package.objects.get(package_name=lead_type).lead_count
        get_wallet_count = get_wallet.remaining_balance
        get_wallet_total_count = get_wallet.total_balance

        get_wallet_count_updated = int(get_wallet_count)+int(get_package_count)
        get_wallet_total_count_updated = int(get_wallet_total_count)+int(get_package_count)
        get_wallet.remaining_balance = str(get_wallet_count_updated)
        get_wallet.total_balance = str(get_wallet_total_count_updated)
        get_wallet.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("Error")



def renew_leads_paypal(request):
    amount = request.GET['amount']
    lead_type = request.GET['type']
    mobile = Vendor_Users.objects.get(Email=request.session['vendor_email']).Mobile
    get_user_country=models.Vendor_Users.objects.get(Email=request.session['vendor_email']).country_name
    get_country_currency=models.Countries.objects.get(name=get_user_country).currency
    currency = get_country_currency

    # momotran.main_call(amount,mobile,currency)
    get_user = Vendor_Users.objects.get(Email = request.session['vendor_email'])
    get_wallet = vendor_wallet_manager.objects.get(vendor_id=get_user.id)
    get_package_count = vendor_leads_package.objects.get(package_name=lead_type).lead_count
    get_wallet_count = get_wallet.remaining_balance
    get_wallet_total_count = get_wallet.total_balance

    get_wallet_count_updated = int(get_wallet_count)+int(get_package_count)
    get_wallet_total_count_updated = int(get_wallet_total_count)+int(get_package_count)
    get_wallet.remaining_balance = str(get_wallet_count_updated)
    get_wallet.total_balance = str(get_wallet_total_count_updated)
    get_wallet.save()
    return HttpResponse("OK")

def quote_pay_confirm(request):
    id = request.GET['id']
    db = request_a_quote.objects.get(id=id)
    db.status = 'Milestone Paid'
    db.save()
    return redirect('proposal_transactions')

def resend_otp_vendor_reg(request):
    digits = [i for i in range(0, 10)]

## initializing a string
    random_str = ""

## we can generate any lenght of string we want
    for i in range(6):
## generating a random index
## if we multiply with 10 it will generate a number between 0 and 10 not including 10
## multiply the random.random() with length of your base list or str
        index = math.floor(random.random() * 10)

        random_str += str(digits[index])
    code_1=''
    count=1
    request.session['vendor_otp']=random_str
    ev_contact = EV_Contact.objects.get(id=1)
    content=render_to_string('vendor_admin1/otp_mail.html', {"fname":request.session['vendor_fname'],"OTP":random_str,"ev_contact":ev_contact})
    send_mail(subject='Authenticate via OTP | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[request.session['email']], html_message=content)
    return HttpResponse("OK")