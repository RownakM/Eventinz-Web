# from pyexpat.errors import messages
# import re
import datetime
from email.quoprimime import quote
import math
import random
import re
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from googletrans import Translator
from urllib3 import HTTPResponse
from Eventinz_Terms_And_Conditions.models import Eventinz_Privacy_Policy, Eventinz_Terms
from Language_Control.models import Language_Control
from Mails.models import User_Welcome_Mail
from about.models import EV_About, Eventinz_Teams
from eventinz_contact_details.models import EV_Contact
from eventmanager.models import create_event_packages, event_budget_settings, event_entries, event_heads_manager, event_planner_CMS, event_reviews_user_to_vendor, vendor_event_proposal, vendor_event_proposal_items
from helloworld.models import NewsLetter

from transaction_records_user.models import Vendor_Payment_History, Vendor_Payment_History_events, user_transaction_records
from .forms import MyForm
from user_dashboard.models import user_login
# Create your views here.
from indexCMS.models import Packages_CMS, Vendor_Categories_Text, Vendor_Deals_Index_CMS, advertisement, how_eventinz_works, index_slider,index_headers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from content_app.models import Exchange_Rates, Exchange_Rates_API, Our_Vendor_CMS, Venue_Type_by_venue, Venue_main_home, cron_activities, event_categories,event_categories_french,event_sub_categories,event_sub_categories_french,Venue_Type,Venue_Details
from vendor_admin.models import Countries, Vendor_FAQ, Vendor_Users, Vendor_bank_listing, request_a_quote, search_cms, total_accepted_orders, total_sales, total_sales_count, vendor_categories, vendor_gallery, vendor_packages, vendor_public_deals, vendor_public_packages, vendor_questions, vendor_quote_invoice,vendor_sub_categories, vendor_subscription
from blogs.models import Blog_Category_Details, Post,blog_category,Blog_CMS,PostImage
from django.db.models import Subquery
from chat.models import Room, Message

def transl(value,fr):
    translator = Translator()
    a=''
    t=''
    db = Language_Control.objects.filter(status = 'Enable')
    if fr == 'Yes':
        ex = ['Eventinz, The Most Reliable Event Resource Platform in West Africa.']
        english = list(db.values_list('english_text',flat=True))
        french = list(db.values_list('french_text',flat=True))

   
        

        if value in english:
            get_index = english.index(value)
            a = french[get_index]
            return a
        else:
            a = translator.translate(value,dest='fr')
            t = a.text
            return t
    else:
        return value
def visitor_ip_address(request):

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
    if 'user_location_track' in request.session:
        pass
    else:

        request.session['user_location_track']=country
   
    if country == 'Bénin':
        country ='Benin'
        request.session['user_location_track']=country


    # request.session['user_country']=country
    # return HttpResponse(country)
    return request.session['user_location_track']
    # return JsonResponse({'lat':str(response.location.latitude),'lon':str(response.location.longitude)})
    
def index(request):
    modal_active=False

    
    if request.method=='POST':
        form=MyForm(request.POST)
        
        if form.is_valid():
            get_url=request.POST['geturl']
            fname=request.POST['fname']
            lname=request.POST['lname']
            email=request.POST['email']
            mno_code=request.POST['mno_code']
            mobile=request.POST['mobile']
            password=request.POST['password']
            re_password=request.POST['re_password']
            countries=request.POST['countries']
            state=request.POST['state']
            city=request.POST['city']
            if (password==re_password):
                user_login(fname=fname,lname=lname,Email=email,password=password,mobile_code=mno_code,mobile=mobile,country=countries,state=state,city=city).save()
                request.session['user_login']=True
                request.session['user_email']=email
                get_mail_db=User_Welcome_Mail.objects.get(id=1)
                # send_mail(
                #     'activation mail',
                #     'message here',
                #     'support@eventinz.com',
                #     [email],
                #     fail_silently=False,
                #     )

                mail_context={
                    'data':get_mail_db,
                    'fname':fname,
                    'is_french':request.session['is_french']
                }
                content=render_to_string('vendor_home/mail_welcome.html',mail_context)
                send_mail(subject=get_mail_db.subject, message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
                return redirect(get_url)
                # messages.info(request,"password matched")

            else:
                messages.info(request,"password not match")
                
            # print("success")
        else:
            modal_active=True
            messages.info(request,"captcha invalid")

            # print("fail")
    form=MyForm()
    user_email=''
    vendor_cat=vendor_categories.objects.all()
    event_categorie=event_categories.objects.all()
    index_slider_text=index_headers.objects.get(id=1).Header
    index_slider_sub_text=index_headers.objects.get(id=1).sub_header
    index_slider_count=index_slider.objects.all().count()
    how_ev_works=how_eventinz_works.objects.get(id=1)
    num_list=[]
    index_slider_models=index_slider.objects.all()
    advertisement_data=advertisement.objects.get(id=1)
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    all_packages=vendor_packages.objects.all()
    req_no_of_random_items = 8        ## i need 8 random items.
    qs = vendor_public_packages.objects.all()
    qs_count = qs.count()
    random_paint=''

    if qs_count > 0:
    ## if u prefer to use random values often, you can keep this in cache. 
    # [ First Query Hit ]
        possible_ids = list(qs.values_list('id', flat=True))        
        possible_ids = random.choices(possible_ids, k=6)
        random_paint = qs.filter(pk__in=possible_ids)
        if qs_count > 6:
            random_paint=vendor_public_packages.objects.all().distinct('package_name')[:6]
    else:
        random_paint=vendor_public_packages.objects.all().distinct('package_name')
    ## in a generic case to get 'n' items.
    for i in range(0,index_slider_count):
        num_list.append(i)
    if 'user_login' in request.session:
        if (request.session['user_login']==True):
            user_email=request.session['user_email']
    else:
        request.session['user_login']=False
    vendor_deals_object=Vendor_Deals_Index_CMS.objects.get(id=1)
    location=visitor_ip_address(request)
    vendor_Categ_text=Vendor_Categories_Text.objects.get(id=1)
    deals=vendor_public_deals.objects.all()

    if 'user_location_track' in request.session:

        location=request.session['user_location_track']
    context={
        'vendor_categories':vendor_cat,
        'adv':advertisement_data,
        
        'index_slider':index_slider_models,
        'how_ev_works':how_ev_works,
        'num_list':num_list,
        "event_categories":event_categorie,
        'index_header':index_slider_text,
        'index_sub_heading':index_slider_sub_text,
        "email":user_email,
        "user_login1":request.session['user_login'],
        "form":form,
        "modal_active":modal_active,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        'packages':random_paint,
        'vendor_deals_object':vendor_deals_object,
        'get_user_location': location,
        'vendor_Categ_text':vendor_Categ_text,
        'deals':deals,
        'is_french':request.session['is_french']


    }
    return render(request,'vendor_home/index.html',context)
def inner_page(request):
    return render(request,'vendor_home/inner-page.html')
def test(request):
    return render(request,'vendor_home/test.html')

def get_sub_categories(request):
    id=request.GET['id']
    sub_categories=event_sub_categories.objects.filter(category=id)
    from django.core import serializers
# serialize queryset
    sub_categories_json = serializers.serialize('json', sub_categories)
    return HttpResponse(sub_categories_json)

def get_sub_category_vendor(request):
    id=request.GET['id']
    sub_categories=vendor_sub_categories.objects.filter(main_category=id)
    from django.core import serializers
# serialize queryset
    sub_categories_json = serializers.serialize('json', sub_categories)
    return HttpResponse(sub_categories_json)
def get_email(request):
    
    from django.http import HttpResponse
    from django.http import JsonResponse
    from django.core import serializers


    import json
    id=request.GET['email']
    qs = user_login.objects.filter(Email=id)
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')

def blogs(request):
    blog_content=Post.objects.filter(status=1)
    blog_categories=blog_category.objects.all()
    blog_cms=Blog_CMS.objects.get(id=1)
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')


    
    context={
        "blog_content": blog_content,
        'blog_category':blog_categories,
        'blog_cms':blog_cms,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        "user_login1":request.session['user_login'],
        'is_french':request.session['is_french']


    }
    return render(request,'vendor_home/blog.html',context)
def get_blog_detail(request,id,name):
    # blog_content=Post.objects.get(status=1,blog_id=id,title=name)
    post = get_object_or_404(Post, blog_id=id)
    # blog_photos=get_object_or_404(Post)
    photos=PostImage.objects.filter(post=post)
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')

    context={
        "blog_content":post,
        "photos":photos,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        "user_login1":request.session['user_login'],
        'is_french':request.session['is_french']


    }
    return render(request,'vendor_home/blog-detail.html',context)

def get_blog_content_page(request,id,name):
    blog_content=Post.objects.filter(status=1,category=id)


    get_blog_details_content=get_object_or_404(Blog_Category_Details,category=id)

    # # blog_content=Post.objects.get(status=1,blog_id=id,title=name)
    # post = get_object_or_404(Post, blog_id=id)
    # # blog_photos=get_object_or_404(Post)
    # photos=PostImage.objects.filter(post=post)
    # venue_links=Venue_Type.objects.all()
    # venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')

    # context={
    #     "blog_content":post,
    #     "photos":photos,
    #     'venue_links':venue_links,
    #     'venue_by_venue':venue_by_venuetype,
    #     "user_login1":request.session['user_login'],


    # }
    context={
        'details':get_blog_details_content,
        'blog_content':blog_content,
        'user_login1':request.session['user_login'],
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/blog-EventCoverage.html',context)

def get_venue(request,venue_type):
    venue_links=Venue_Type.objects.all()
    get_venue_id=Venue_Type.objects.get(venue_name=venue_type).id
    venue_content=Venue_Details.objects.get(venue_name=get_venue_id)
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    get_user_venues=Vendor_Users.objects.filter(event_category_serve__has_key=venue_type,vendor_categories__has_key='Venue')
    get_user_count=get_user_venues.count()

    context={
        'venue_type':venue_type.title(),
        'venue_links':venue_links,
        'venue_contents':venue_content,
        'venue_by_venue':venue_by_venuetype,
        'get_user_venues':get_user_venues,
        'get_user_count':get_user_count,
        "user_login1":request.session['user_login'],
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/weddings.html',context)


def get_venues(request):
    venue_links=Venue_Type.objects.all()
    # get_venue_id=Venue_Type.objects.get(venue_name=venue_type).id
    # venue_content=Venue_Details.objects.get(venue_name=get_venue_id)
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    main_venue_header=Venue_main_home.objects.get(id=1)
    
    
    context={
        # 'venue_type':venue_type.title(),
        'venue_links':venue_links,
        # 'venue_contents':venue_content,
        'venue_by_venue':venue_by_venuetype,
        'main_venue_header':main_venue_header,
        'is_french':request.session['is_french']
        
    }
    return render(request,'vendor_home/venues_home.html',context)
    # return redirect('vendor_home:vendor_home_index')

def get_single_venue(request,venue_type,list_id,title):
    if 'user_login' not in request.session:
        request.session['user_login']=False
    id=list_id
    venue_type=venue_type
    title=title
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')

    get_vendor_company=Vendor_Users.objects.get(id=id)
    get_vendor_email=get_vendor_company.Email
    get_vendor_package=vendor_public_packages.objects.filter(vendor_id=get_vendor_email,category_name=venue_type).distinct('package_name')
    get_gallery=vendor_gallery.objects.filter(category_name=venue_type,vendor_email=get_vendor_email)
    get_gallery_count=vendor_gallery.objects.filter(category_name=venue_type,vendor_email=get_vendor_email).count()
    get_features_list=get_vendor_company.question_field
    get_cater_list=get_vendor_company.caterer_field
    get_vendor_categories=vendor_subscription.objects.get(vendor_email=get_vendor_email).vendor_categories
    li = list(get_vendor_categories.split("__#__"))
    category_list=[]
    for i in li:
        if i == '':
            break
        get_category_name=vendor_categories.objects.get(id=i).category_name
        category_list.append(get_category_name)
    req_count=True
    req_status=''
    from django.core.exceptions import ObjectDoesNotExist

    if 'user_email' in request.session:
        try:
            get_req_quote_count=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id,status='pending').count()
  # try something
        except ObjectDoesNotExist:
            get_req_quote_count=0

        # get_req_status=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id)
        if get_req_quote_count > 0:
            req_count=True
        else:
            try:
                get_req_type=request_a_quote.objects.get(email=request.session['user_email'],vendor_id=id).status
            except ObjectDoesNotExist:
                get_req_type=None
            req_count=False
            if get_req_type=='accept':
                req_status=True
            elif get_req_type=='reject':
                req_status=False
    else:
        req_count=False
    user_acc=''
    if 'user_login' in request.session:
        if request.session['user_login']==True:
            user_acc=user_login.objects.get(Email=request.session['user_email'])
        else:
            user_acc=''
    else:
        user_acc=''

    context={
        "company_details":get_vendor_company,
        "vendor_package":get_vendor_package,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        'get_gallery':get_gallery,
        'get_gallery_count':get_gallery_count,
        "get_features_list":get_features_list,
        'get_cater_list':get_cater_list,
        "vendor_category":category_list,
        "user_login":request.session['user_login'],
        "req_stats":req_count,
        'user_acc':user_acc,
        'req_status':req_status,
        'venue_type':venue_type,
        "user_login1":request.session['user_login'],
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french']


    }
    return render(request,'vendor_home/vendor.html',context)


def get_location(request,lon,lat):
    from geopy.geocoders import Nominatim
 
# initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")
 
 
# Latitude & Longitude input
    Latitude = lat
    Longitude = lon
 
    location = geolocator.reverse(Latitude+","+Longitude)
 
    address = location.raw['address']
 
# traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    code = address.get('country_code')
    zipcode = address.get('postcode')
   
    request.session['user_location_track']=country
   
    if country == 'Bénin':
        country ='Benin'
        request.session['user_location_track']=country


    # request.session['user_country']=country
    return HttpResponse(country)
# print('State : ', state)
# print('Country : ', country)
# print('Zip Code : ', zipcode)

def get_location_new(request):
    return HttpResponse("OK")

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def request_quote(request):
    email=request.GET['email']
    fname=request.GET['fname']
    lname=request.GET['lname']
    event_type=request.GET['event_type']
    event_date=request.GET['event_date']
    guests=request.GET['guests']
    msg=request.GET['msg']
    vendor_id=int(request.GET['vendor_id'])
    v_link=request.GET['v_link']
    request_a_quote(fname=fname,lname=lname,email=email,phone='123',v_link=v_link,event_type=event_type,appx_date=event_date,no_of_guests=guests,msg=msg,vendor_id=Vendor_Users.objects.get(id=vendor_id)).save()

    data = {
        'email':email,
        'fname':fname,
        'lname':lname,
        'event_type':event_type,
        'event_date':event_date,
        'guests':guests,
        'msg':msg,
        'vendor_id':vendor_id,
        'date':datetime.date.today(),
        'phone':Vendor_Users.objects.get(id=vendor_id).Mobile,
        'phone_code':Vendor_Users.objects.get(id=vendor_id).phone_code
    }
    content=render_to_string('vendor_home/request-quote-success.html',data)
    send_mail(subject='Quote Requested ! | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
    # request.session[]
    return HttpResponse(email)

def deals(request):
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    deals=vendor_public_deals.objects.all()
    context={
        "user_login1":request.session['user_login'],
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        'deals':deals,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/deal_page.html',context)


def user_login_view(request):
    if request.method=='POST':
        user_email=request.POST['user_mail']
        user_password=request.POST['user_password']
        # try:
        #     user_data=user_login.objects.filter(Email=user_email)
        #     if user_data.exists():

        #         user_data=user_login.objects.get(Email=user_email)
        #     else:
        #         user_data

        site_path=request.POST['site_path']
        user_data = user_login.objects.filter(Email=user_email)
        if not user_data.exists():
            messages.error(request,'Wrong Credentials')
            return redirect(site_path)
        else:
            user_data = user_login.objects.get(Email=user_email)
        user_password_1=user_data.password
        if user_password_1==user_password:
            request.session['user_login']=True
            request.session['user_email']=user_email
            return redirect(site_path)
        else:
            messages.error(request,'Wrong Credentials')
            return redirect(site_path)
            # return HttpResponse("Error")


def user_profile(request):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        total_event=event_entries.objects.filter(Email=user_email)
        total_event_count=total_event.count()
        ongoing_event=event_entries.objects.filter(Email=user_email,status='Hired')
        ongoing_event_count=ongoing_event.count()
        complete_event=event_entries.objects.filter(Email=user_email,status="Complete")
        complete_event_count=complete_event.count()
        cancel_event=event_entries.objects.filter(Email=user_email,status="cancel")
        cancel_event_count=cancel_event.count()


        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'events':total_event,
            'event_count':total_event_count,
            'ongoing_event_count':ongoing_event_count,
            "complete_event_count":complete_event_count,
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french'],
            'cancel_event_count':cancel_event_count,
            'user_id':get_user.id
        }
        return render(request,'user_dashboard_v2/dashboard.html',context)
    else:
        return redirect('vendor_home:vendor_home_index')

def my_events_all(request):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        total_event=event_entries.objects.filter(Email=user_email)
        total_event_count=total_event.count()
        ongoing_event=event_entries.objects.filter(Email=user_email,status='Hired')
        ongoing_event_count=ongoing_event.count()

        complete_event=event_entries.objects.filter(Email=user_email,status="Complete")
        complete_event_count=complete_event.count()

        cancel_event=event_entries.objects.filter(Email=user_email,status="cancel")
        cancel_event_count=cancel_event.count()

        archieve_event = event_entries.objects.filter(Email=user_email,is_archieve = True)
        archieve_event_count = archieve_event.count()

        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'events':total_event.distinct('unique_id'),
            'event_count':total_event_count,
            'ongoing_event_count':ongoing_event_count,
            "complete_event_count":complete_event_count,
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french'],
            'cancel_event_count':cancel_event_count,
            'archieve_event_count':archieve_event_count
        }
        return render(request,'user_dashboard_v2/dashboard-my-events-page.html',context)
def my_events_all_unarchieve(request):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        total_event=event_entries.objects.filter(Email=user_email)
        total_event_count=total_event.count()
        ongoing_event=event_entries.objects.filter(Email=user_email,status='Hired')
        ongoing_event_count=ongoing_event.count()

        complete_event=event_entries.objects.filter(Email=user_email,status="Complete")
        complete_event_count=complete_event.count()

        cancel_event=event_entries.objects.filter(Email=user_email,status="cancel")
        cancel_event_count=cancel_event.count()

        archieve_event = event_entries.objects.filter(Email=user_email,is_archieve = True)
        archieve_event_count = archieve_event.count()

        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'events':total_event,
            'event_count':total_event_count,
            'ongoing_event_count':ongoing_event_count,
            "complete_event_count":complete_event_count,
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french'],
            'cancel_event_count':cancel_event_count,
            'archieve_event_count':archieve_event_count
        }
        return render(request,'user_dashboard_v2/dashboard-my-event-page-archieve.html',context)
def my_events_open(request):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        total_event=event_entries.objects.filter(Email=user_email,status='draft')
        total_event_count=total_event.count()


        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'events':total_event,
            'event_count':total_event_count,
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french']
        }
        return render(request,'user_profile/my_events_open.html',context)
def my_events_closed(request):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        total_event=event_entries.objects.filter(Email=user_email,status='closed')
        total_event_count=total_event.count()


        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'events':total_event,
            'event_count':total_event_count,
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french']
        }
        return render(request,'user_profile/my_events_closed.html',context)

def my_events_progress(request):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        total_event=event_entries.objects.filter(Email=user_email,status='progress')
        total_event_count=total_event.count()


        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'events':total_event,
            'event_count':total_event_count,
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french']
        }
        return render(request,'user_profile/my_events_progress.html',context)

# from django import register
from qr_code.qrcode.utils import QRCodeOptions
def invoice1(request):
    quote_id=request.GET['quote_id']
    quotes_data=vendor_quote_invoice.objects.get(quote_id=quote_id)
    quotes_data_set=vendor_quote_invoice.objects.filter(quote_id=quote_id)
    my_options=QRCodeOptions(size='m', border=6, error_correction='M')

    context={
        'quotes_data':quotes_data,
        'quotes_data_set':quotes_data_set,
        'my_options':my_options,
        'get_user_location':request.sessionvisitor_ip_address(request),
        'is_french':request.session['is_french']
    }

    return render(request,'invoices/invoice-eventinz.html',context)

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
def invoice(request):
    quote_id=request.GET['quote_id']
    quotes_data=vendor_quote_invoice.objects.get(quote_id=quote_id)
    quotes_data_set=vendor_quote_invoice.objects.filter(quote_id=quote_id)
    my_options=QRCodeOptions(size='m', border=6, error_correction='M')

    template_path = 'invoices/invoice-eventinz.html'
    context={
        'quotes_data':quotes_data,
        'quotes_data_set':quotes_data_set,
        'my_options':my_options,
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french']
    }
    return render(request,template_path,context)
    # context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    # response = HttpResponse(content_type='application/pdf')
    # # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # response['Content-Disposition'] = 'filename='+str(quote_id)+'.pdf'

    # # find the template and render it.
    # template = get_template(template_path)
    # html = template.render(context)

    # # create a pdf
    # pisa_status = pisa.CreatePDF(
    #    html, dest=response)
    # # if error then show some funny view
    # if pisa_status.err:
    #    return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response

def user_chat(request,quote_id):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        import uuid
        id=quote_id
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=request_a_quote.objects.filter(email=user_email).order_by('-created_on')
        user_quote_req_count=request_a_quote.objects.filter(email=user_email).count()
        username = get_user.fname # henry
        username1= request_a_quote.objects.get(id=quote_id).vendor_id.Company_Name
        room='EV-Rooms-'+str(username)

        room_details = Room.objects.get_or_create(name=room,quote_id=id)
        room_details = Room.objects.get(name=room,quote_id=id)

    #     return render(request, 'room.html', {

        
    # })

        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'room':room,
            'username': username,

        # 'room': room,
            'room_details': room_details,
            'quote_id':id,
            'is_french':request.session['is_french'],
            'username1':username1
        }

        return render(request,'user_dashboard_v2/dashboard-chat-quote.html',context)



def user_chat_events(request,event_id):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        country=get_user.country
        # get_country=Countries.objects.get(id=get_user.country).name
        import requests

        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
          'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        # print(response.text)
        import json
        import uuid
        id=event_id
        data=json.loads(response.text)
        get_country=data['name']
        user_quote_req=event_entries.objects.filter(Email=user_email).order_by('-created_on')
        user_quote_req_count=event_entries.objects.filter(Email=user_email).count()
        username = get_user.fname # henry
        room='EV-Rooms-Event'+str(username)

        room_details = Room.objects.get_or_create(name=room,quote_id=id)
        room_details = Room.objects.get(name=room,quote_id=id)

    #     return render(request, 'room.html', {

        
    # })

        context={
            'user':get_user,
            'country':get_country,
            'get_quotes':user_quote_req,
            "user_quote_req_count":user_quote_req_count,
            'room':room,
            'username': username,

        # 'room': room,
            'room_details': room_details,
            'quote_id':id,
            'is_french':request.session['is_french']
        }

        return render(request,'user_dashboard_v2/dashboard_chat_popup.html',context)

def chat_dup(request):
    return HttpResponse("OK")

def create_event(request):
    import json
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    form=MyForm()
    event_cat=event_categories.objects.all()
    budget_settings=event_budget_settings.objects.all()
    head_settings=event_heads_manager.objects.all()
    event_packages=create_event_packages.objects.get(id=1)
    vendor_types=vendor_categories.objects.all()
    # import requests

    #     # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+event_packages.currency_country.currency

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()
    user_currency=Countries.objects.get(name=visitor_ip_address(request)).currency
    # ex_value=Exchange_Rates.objects.get(base_country=event_packages.currency_country.currency,dest_country=user_currency).ex_rate
    # onefcfa=float(ex_value)

    # ex_value=Exchange_Rates.objects.get(base_country=get_currency_vendor,dest_country=get_user_currency).ex_rate


    import requests

    url = 'https://api.exchangerate.host/convert?from='+event_packages.currency_country.currency+'&to='+user_currency
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    # onefcfa=float(data['conversion_rates'][user_currency])

    freemium_pack='0.00'
    premium_pack=round((event_packages.premium_amount)*(onefcfa),2)

    user_login1=''
    user=''
    if 'user_login' in request.session:
        user_login1=request.session['user_login']
        if 'user_email' in request.session:
            user=user_login.objects.get(Email=request.session['user_email'])

    is_benin = False
    cntry = request.session['user_location_track']
    if cntry == "Benin":
        is_benin = True
    
    context={
        "user_login1":user_login1,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        'form':form,
        'event_categories':event_cat,
        'budget_settings':budget_settings,
        'event_heads':head_settings,
        'get_user_location':visitor_ip_address(request),
        'event_packages':event_packages,
        'freemium_pack':freemium_pack,
        'premium_pack':premium_pack,
        'momo_pack':event_packages.premium_amount,
        'user_currency':user_currency,
        'vendor_categories':vendor_types,
        'user':user,
        'is_french':request.session['is_french'],
        'cntry':is_benin
        
    }
    return render(request,'user_profile/create_event.html',context)

def accept_quote(request):
    id=request.GET['id']
    db=request_a_quote.objects.get(id=id)
    db.status='Done'
    db.save()
    return HttpResponse("Done")
def reject_quote(request):
    id=request.GET['id']
    db=request_a_quote.objects.get(id=id)
    db.status='Declined'
    db.save()
    return HttpResponse("Done")

def save_transaction_record(request):
    quote_id=request.GET['quote_id']
    transaction_id=request.GET['transaction_id']
    amount=request.GET['amount']
    transaction_type=request.GET['transaction_type']
    pay_type=int(request.GET['pay_type'])
    if pay_type == 2:

        db=user_transaction_records(quote_id=request_a_quote.objects.get(id=quote_id),transaction_id=transaction_id,transaction_amount=amount,transaction_type=transaction_type,remarks='2')
    else:
        db=user_transaction_records(quote_id=request_a_quote.objects.get(id=quote_id),transaction_id=transaction_id,transaction_amount=amount,transaction_type=transaction_type,email=request.session['user_email'])

    db_req=request_a_quote.objects.get(id=quote_id)
    if pay_type == 2:
        db_req.status='2nd Milestone Paid'
        vid=db_req.vendor_id.Email
        a=total_sales_count.objects.get(vendor_id=vid)
        a.total_count+=1
        a.save()
        b=total_sales.objects.get(vendor_id=vid)
        from datetime import datetime
        currentMonth = datetime.now().month
        if currentMonth == 1:
            b.Jan_sales+=1
            b.save()
        if currentMonth == 2:
            b.Feb_sales+=1
            b.save()
        if currentMonth == 3:
            b.Mar_sales+=1
            b.save()
        if currentMonth == 4:
            b.Apr_sales+=1
            b.save()
        if currentMonth == 5:
            b.May_sales+=1
            b.save()
        if currentMonth == 6:
            b.Jun_sales+=1
            b.save()
        if currentMonth == 7:
            b.Jul_sales+=1
            b.save()
        if currentMonth == 8:
            b.Aug_sales+=1
            b.save()
        if currentMonth == 9:
            b.Sep_sales+=1
            b.save()
        if currentMonth == 10:
            b.Oct_sales+=1
            b.save()
        if currentMonth == 11:
            b.Nov_sales+=1
            b.save()
        if currentMonth == 12:
            b.Dec_sales+=1
            b.save()
        


    else:
        db_req.status='Milestone Paid'
        

    db_req.save()
    db.save()
    save_wallet=user_login.objects.get(Email=request.session['user_email'])
    save_wallet.user_wallet=float(save_wallet.user_wallet)+float(amount)
    save_wallet.save()
    return HttpResponse("Done")


def events(request):
    events_planners=event_categories.objects.all()
    event_cms=event_planner_CMS.objects.get(id=1)
    user_login=''
    if 'user_login' in request.session:
        user_login=request.session['user_login']
    else:
        user_login='no'
    context={
        'event_planners':events_planners,
        'event_cms':event_cms,
        'is_french':request.session['is_french'],
        'user_login1':user_login
    }
    return render(request,'vendor_home/events.html',context)
def get_event_planners(request,venue_type):
    venue_links=Venue_Type.objects.all()
    get_venue_id=Venue_Type.objects.get(venue_name=venue_type).id
    venue_content=Venue_Details.objects.get(venue_name=get_venue_id)
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    get_user_venues=Vendor_Users.objects.filter(event_category_serve__has_key=venue_type,vendor_categories__has_key='Event Planner')
    get_user_count=get_user_venues.count()
    user_login=''
    if 'user_login' in request.session:
        user_login=request.session['user_login']
    else:
        user_login='no'
    vendor_features = vendor_questions.objects.filter(Question_Category=vendor_categories.objects.get(id=20).id)
    context={
        'venue_type':venue_type.title(),
        'venue_links':venue_links,
        'venue_contents':venue_content,
        'venue_by_venue':venue_by_venuetype,
        'get_user_venues':get_user_venues,
        'get_user_count':get_user_count,
        "user_login1":user_login,
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french'],
        'vendor_features':vendor_features
    }
    return render(request,'vendor_home/event_search.html',context)

def our_vendors(request):
    vendor_cat=vendor_categories.objects.all()
    vendor_cat_count=vendor_cat.count()
    vendor_cms=Our_Vendor_CMS.objects.get(id=1)
    user_login=''
    if 'user_login' in request.session:
        user_login=request.session['user_login']
    else:
        user_login='no'
    context={
        'vendor_categories':vendor_cat,
        'vendor_cat_count':vendor_cat_count,
        'vendor_cms':vendor_cms,
        'is_french':request.session['is_french'],
        'user_login1':user_login
    }
    return render(request,'vendor_home/our_vendors.html',context)

def get_vendor(request,type_vendor):
    if type_vendor == 'Venue':
        return redirect('vendor_home:Venue')
    if type_vendor == 'Event Planner':
        return redirect('vendor_home:events')
    
   
    venue_links=vendor_categories.objects.all()
    get_venue_id=vendor_categories.objects.get(category_name=type_vendor).id
    venue_content=search_cms.objects.get(category_name=get_venue_id)
    event_links=event_categories.objects.all()
    # venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
    get_user_venues=Vendor_Users.objects.filter(vendor_categories__has_key=type_vendor)
    get_user_count=get_user_venues.count()
    user_login=''
    if 'user_login' in request.session:
        user_login=request.session['user_login']
    else:
        user_login=''

    context={
        'venue_type':type_vendor.title(),
        'venue_links':event_links,
        'venue_contents':venue_content,
        'fix_link':type_vendor,
        # 'venue_by_venue':venue_by_venuetype,
        'get_user_venues':get_user_venues,
        'get_user_count':get_user_count,
        "user_login1":user_login,
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/get_events.html',context)
def get_vendor_url(request,type_vendor,event_type):
    get_vendor_cat_id=vendor_categories.objects.get(category_name=type_vendor).id
    get_vendor_cat=search_cms.objects.get(category_name=get_vendor_cat_id)
    get_user_venues=Vendor_Users.objects.filter(event_category_serve__has_key=event_type,vendor_categories__has_key=type_vendor,country_name=visitor_ip_address(request))
    get_user_count=get_user_venues.count()
    user_login=''
    if 'user_login' in request.session:
        user_login=request.session['user_login']
    else:
        user_login=''
    vendor_features = vendor_questions.objects.filter(Question_Category=get_vendor_cat_id)
    
    context={
        'venue_type':type_vendor.title(),
        # 'venue_links':venue_links,
        'venue_contents':get_vendor_cat,
        # 'venue_by_venue':venue_by_venuetype,
        'get_user_venues':get_user_venues,
        'get_user_count':get_user_count,
        "user_login1":user_login,
        'get_user_location':visitor_ip_address(request),
        'country':visitor_ip_address(request),
        'is_french':request.session['is_french'],
        'vendor_features':vendor_features
    }
    return render(request,'vendor_home/event_search.html',context)

def get_vendor_profile(request,type_vendor,event_type,id_vendor,name_vendor):

    if 'user_login' not in request.session:
        request.session['user_login']=False
    id=id_vendor
    venue_type=type_vendor
    title=name_vendor
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')

    get_vendor_company=Vendor_Users.objects.get(id=id)
    clicks=get_vendor_company.profile_clicks
    get_vendor_company.profile_clicks=clicks+1
    get_vendor_company.save()

    get_vendor_email=get_vendor_company.Email
    get_vendor_package=vendor_public_packages.objects.filter(vendor_id=get_vendor_email,category_name=event_type).distinct('package_name')
    get_gallery=vendor_gallery.objects.filter(category_name=event_type,vendor_email=get_vendor_email)
    get_gallery_count=vendor_gallery.objects.filter(category_name=event_type,vendor_email=get_vendor_email).count()
    get_features_list=get_vendor_company.question_field
    get_cater_list=get_vendor_company.caterer_field
    get_vendor_categories=vendor_subscription.objects.get(vendor_email=get_vendor_email).vendor_categories
    li = list(get_vendor_categories.split("__#__"))
    category_list=[]
    category_list_id=li
    vendor_reviews = event_reviews_user_to_vendor.objects.filter(vendor_id=id_vendor)

    for i in li:
        if i == '':
            break
        get_category_name=vendor_categories.objects.get(id=i).category_name
        
        category_list.append(get_category_name)
    
    try:
        get_blog_categories=blog_category.objects.filter(id__in=category_list_id).values_list('id', flat=True)
        get_blog_post=Post.objects.filter(category__in=get_blog_categories)
    except ValueError:

        get_blog_categories=''
        get_blog_post=''
    get_related_vendors=Vendor_Users.objects.filter(vendor_categories__has_key=type_vendor,country_name=visitor_ip_address(request))


    # get_related_blogs=Post.objects.filter(vendor_category__in=category_list)
    # get_related_blogs_category=blog_category.objects.filter(vendor_category__in=caete)
    req_count=True
    req_status=''
    from django.core.exceptions import ObjectDoesNotExist

    if 'user_email' in request.session:
        try:
            get_req_quote_count=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id,status='pending').count()
  # try something
        except ObjectDoesNotExist:
            get_req_quote_count=0

        # get_req_status=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id)
        if get_req_quote_count > 0:
            req_count=True
        else:
            try:
                # get_req_type=request_a_quote.objects.get(email=request.session['user_email'],vendor_id=id).status
                get_req_type = None
            except ObjectDoesNotExist:
                get_req_type=None
            
            req_count=False
            if get_req_type=='accept':
                req_status=True
            elif get_req_type=='reject':
                req_status=False
    else:
        req_count=False
    user_acc=''
    if 'user_login' in request.session:
        if request.session['user_login']==True:
            user_acc=user_login.objects.get(Email=request.session['user_email'])
        else:
            user_acc=''
    else:
        user_acc=''
    


    if 'user_email' in request.session:
        try:
            get_req_quote_count=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id,status='pending').count()
  # try something
        except ObjectDoesNotExist:
            get_req_quote_count=0

        # get_req_status=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id)
        if get_req_quote_count > 0:
            req_count=True
        else:
            try:
                get_req_type=request_a_quote.objects.get(email=request.session['user_email'],vendor_id=id).status
            except ObjectDoesNotExist:
                get_req_type=None
            req_count=False
            if get_req_type=='accept':
                req_status=True
            elif get_req_type=='reject':
                req_status=False
    else:
        req_count=False
    context={
        "company_details":get_vendor_company,
        "vendor_package":get_vendor_package,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        'get_gallery':get_gallery,
        'get_gallery_count':get_gallery_count,
        "get_features_list":get_features_list,
        'get_cater_list':get_cater_list,
        "vendor_category":category_list,
        "user_login":request.session['user_login'],
        "req_stats":req_count,
        'user_acc':user_acc,
        'req_status':req_status,
        'venue_type':venue_type,
        'get_related_blogs':get_blog_post,
        "user_login1":request.session['user_login'],
        'get_user_location':visitor_ip_address(request),
        'other_related_vendors':get_related_vendors,
        'is_french':request.session['is_french'],
        'vendor_reviews':vendor_reviews


    }
    return render(request,'vendor_home/get_vendor.html',context)

def get_vendor_profile_search(request,id_vendor,name_vendor):

    if 'user_login' not in request.session:
        request.session['user_login']=False
    id=id_vendor
    
    title=name_vendor
    venue_links=Venue_Type.objects.all()
    venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')

    get_vendor_company=Vendor_Users.objects.get(id=id)
    clicks=get_vendor_company.profile_clicks
    get_vendor_company.profile_clicks=clicks+1
    get_vendor_company.save()

    get_vendor_email=get_vendor_company.Email
    get_vendor_package=vendor_public_packages.objects.filter(vendor_id=get_vendor_email).distinct('package_name')
    get_gallery=vendor_gallery.objects.filter(vendor_email=get_vendor_email)
    get_gallery_count=vendor_gallery.objects.filter(vendor_email=get_vendor_email).count()
    get_features_list=get_vendor_company.question_field
    get_cater_list=get_vendor_company.caterer_field
    get_vendor_categories=vendor_subscription.objects.get(vendor_email=get_vendor_email).vendor_categories
    li = list(get_vendor_categories.split("__#__"))
    category_list=[]
    vendor_reviews = event_reviews_user_to_vendor.objects.filter(vendor_id=id_vendor)
    for i in li:
        if i == '':
            break
        get_category_name=vendor_categories.objects.get(id=i).category_name
        category_list.append(get_category_name)
    req_count=True
    req_status=''
    from django.core.exceptions import ObjectDoesNotExist

    if 'user_email' in request.session:
        try:
            get_req_quote_count=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id,status='pending').count()
  # try something
        except ObjectDoesNotExist:
            get_req_quote_count=0

        # get_req_status=request_a_quote.objects.filter(email=request.session['user_email'],vendor_id=id)
        if get_req_quote_count > 0:
            req_count=True
        else:
            try:
                get_req_type=request_a_quote.objects.get(email=request.session['user_email'],vendor_id=id).status
            except ObjectDoesNotExist:
                get_req_type=None
            req_count=False
            if get_req_type=='accept':
                req_status=True
            elif get_req_type=='reject':
                req_status=False
    else:
        req_count=False
    user_acc=''
    if 'user_login' in request.session:
        if request.session['user_login']==True:
            user_acc=user_login.objects.get(Email=request.session['user_email'])
        else:
            user_acc=''
    else:
        user_acc=''

    context={
        "company_details":get_vendor_company,
        "vendor_package":get_vendor_package,
        'venue_links':venue_links,
        'venue_by_venue':venue_by_venuetype,
        'get_gallery':get_gallery,
        'get_gallery_count':get_gallery_count,
        "get_features_list":get_features_list,
        'get_cater_list':get_cater_list,
        "vendor_category":category_list,
        "user_login":request.session['user_login'],
        "req_stats":req_count,
        'user_acc':user_acc,
        'req_status':req_status,
        
        "user_login1":request.session['user_login'],
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french'],
        'vendor_reviews':vendor_reviews


    }
    return render(request,'vendor_home/get_vendor.html',context)

def vendor_search(request):
    if request.method=='POST':
        category_id=request.POST['category_vendor']
        subcategory=request.POST['subcategory_vendor']
        category_name=vendor_categories.objects.get(id=category_id).category_name
        category_image = vendor_categories.objects.get(id=category_id).category_cover_image
        venue_links=Venue_Type.objects.all()
        # get_venue_id=Venue_Type.objects.get(venue_name=venue_type).id
        # venue_content=Venue_Details.objects.get(venue_name=get_venue_id)
        # venue_by_venuetype=Venue_Type_by_venue.objects.filter().order_by('id')
        if (subcategory != 'all'):
            get_user_venues=Vendor_Users.objects.filter(vendor_categories__has_key=category_name,country_name=visitor_ip_address(request),vendor_sub_cat_data__icontains=subcategory)
        else:
            get_user_venues=Vendor_Users.objects.filter(vendor_categories__has_key=category_name,country_name=visitor_ip_address(request))

        get_user_count=get_user_venues.count()
        vendor_features = vendor_questions.objects.filter(Question_Category=vendor_categories.objects.get(id=category_id).id)
        context={
            'venue_type':category_name.title(),
            'venue_links':venue_links,
            # 'venue_contents':venue_content,
            # 'venue_by_venue':venue_by_venuetype,
            'get_user_venues':get_user_venues,
            'get_user_count':get_user_count,
            "user_login1":request.session['user_login'],
            'get_user_location':visitor_ip_address(request),
            'is_french':request.session['is_french'],
            "category_image":category_image,
            'vendor_features':vendor_features
        }
        return render(request,'vendor_home/search.html',context)
    else:

        return redirect('vendor_home:vendor_home_index')

def user_profile_logout(request):
    url = str(request.GET['url'])
    del request.session['user_login']
    del request.session['user_email']
    return redirect(str(url))

def get_event_sub_cat(request):
    from django.http import JsonResponse
    import json
    event_id=request.GET['event_category_id']
    sub_cat=event_sub_categories.objects.filter(category=event_id)
    from django.core import serializers

    sub_cat_data=serializers.serialize('json', sub_cat)
    return HttpResponse(sub_cat_data,content_type="application/json")

def ev_send_mail(request):
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
    
    otp=random_str
    request.session['create_event_otp']=otp

    # storing data

    request.session['create_event_country']=request.GET['country']
    request.session['create_event_state']=request.GET['state']
    request.session['create_event_city']=request.GET['city']
    request.session['create_event_event_category']=request.GET['event_category']
    request.session['create_event_event_sub_category']=request.GET['event_sub_category']
    request.session['create_event_heads']=request.GET['heads']
    request.session['create_event_ev_date']=request.GET['ev_date']
    request.session['create_event_budget']=request.GET['budget']
    request.session['create_event_first_name']=request.GET['first_name']
    request.session['create_event_last_name']=request.GET['last_name']
    request.session['create_event_email_id']=request.GET['email_id']
    request.session['create_event_phone']=request.GET['phone']
    request.session['create_event_country_code']=request.GET['country_code']
    request.session['create_event_ev_desc']=request.GET['ev_desc']
    get_ev_name=event_categories.objects.get(id=request.GET['event_category']).category_name
    request.session['get_ev_name']=get_ev_name

    is_updated=request.GET['updated']
    if(is_updated != 'YES'):
        content=render_to_string('vendor_home/event_otp.html',{'otp':otp})
        send_mail(subject='Authenticate via OTP - Eventinz | Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[request.GET['email_id']], html_message=content)
        return HttpResponse("OK")

    else:
        return HttpResponse("OK")


def ev_check_otp(request):
    recieved_otp=request.GET['otp']
    ev_mail=request.session['create_event_email_id']
    send_otp=request.session['create_event_otp']
    if recieved_otp == send_otp:
        db=user_login.objects.filter(Email=ev_mail)
        if db.exists():

            return HttpResponse("checkpwd")
        else:
            return HttpResponse('Newuser')
    else:
        return HttpResponse("NO")


def ev_check_pwd(request):
    email=request.session['create_event_email_id']
    pwd_recieved=request.GET['pwd']
    db=user_login.objects.get(Email=email)
    pwd_stored=db.password
    if str(pwd_stored) == str(pwd_recieved):
        country=request.session['create_event_country']
        state=request.session['create_event_state']
        city=request.session['create_event_city']
        event_category=request.session['create_event_event_category']
        event_sub_category=request.session['create_event_event_sub_category']
        heads=request.session['create_event_heads']
        ev_date=request.session['create_event_ev_date']
        budget=request.session['create_event_budget']
        first_name=request.session['create_event_first_name']
        last_name=request.session['create_event_last_name']
        email_id=request.session['create_event_email_id']
        phone=request.session['create_event_phone']
        country_code=request.session['create_event_country_code']
        ev_desc=request.session['create_event_ev_desc']
        
        request.session['user_login']=True
        request.session['user_email']=email_id


        event_category_name=event_categories.objects.get(id=event_category).category_name
        b=event_sub_category[1:-1]
        c=b.split(',')
        subcategories_data={}
        count=0
        for i in c:
            id=int(i[1:-1])
            sub_cat_name=event_sub_categories.objects.get(id=id).sub_category_name
            subcategories_data[int(count)]=transl(value=str(sub_cat_name),fr=request.session['is_french'])
            count+=1


        response_data={}

        import requests
        import json
        url = "https://api.countrystatecity.in/v1/countries/"+country

        headers = {
        'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
        }

        response = requests.request("GET", url, headers=headers)

        data=response.text
        data_json=json.loads(data)
        import datetime 
        get_validity = create_event_packages.objects.get(id=1).premium_validity
        tod = datetime.datetime.now()
        d = datetime.timedelta(days = get_validity)
        a = tod - d
        b = tod + datetime.timedelta(days = 1)
        check_date_min=a.date()
        check_date_max=b.date()
        check_subscription = event_entries.objects.filter(created_on__range=[check_date_min,check_date_max],Email=email_id,user_type='premium')
        if check_subscription.exists():
            response_data['status']='Subscription Exists'
        else:
            response_data['status']='OK'
        response_data['country']=data_json['name']
        url = "https://api.countrystatecity.in/v1/countries/"+country+"/states/"+state
        response = requests.request("GET", url, headers=headers)

        data=response.text
        data_json=json.loads(data)
        response_data['state']=data_json['name']
        url = "https://api.countrystatecity.in/v1/countries/"+country+"/states/"+state+"/cities"
        response = requests.request("GET", url, headers=headers)
        data=response.text
        data_json=json.loads(data)
        count=0
        response_data['city']=''
        for i in range(0,len(data_json)):
            if data_json[i]['id'] == int(city):
                response_data['city']=data_json[i]['name']
                count+=1
                
        response_data['event_category']=transl(str(event_category_name),request.session['is_french'])
        response_data['sub_category']=subcategories_data
        heads_data=event_heads_manager.objects.get(id=heads)

        response_data['heads']=str(heads_data.Minimum_Value)+' - '+str(heads_data.Maximum_Value)
        response_data['ev_date']=ev_date
        get_budget_data=event_budget_settings.objects.get(id=budget)
        user_country=Countries.objects.get(name=visitor_ip_address(request)).currency
        # import requests

        # # Where USD is the base currency you want to use
        # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+get_budget_data.country.currency

        #     # Making our request
        # response = requests.get(url)
        # data = response.json()
        # ex_value=Exchange_Rates.objects.get(base_country=get_budget_data.country.currency,dest_country=user_country).ex_rate
        # onefcfa=float(ex_value)



        import requests

        url = 'https://api.exchangerate.host/convert?from='+get_budget_data.country.currency+'&to='+user_country
        response = requests.get(url)
        data = response.json()
        onefcfa=float(data['info']['rate'])


        # onefcfa=float(data['conversion_rates'][str(user_country)])

        budget_minimum=round((get_budget_data.Minimum_Value)*(onefcfa),2)
        if (get_budget_data.Maximum_Value != 2441139):
            budget_maximum = 'Above'
            response_data['budget']='Above '+str(budget_minimum)

        else:
            budget_maximum=round((get_budget_data.Maximum_Value)*(onefcfa),2)
            response_data['budget']=user_country+' '+str(budget_minimum)+' - '+user_country+' '+str(budget_maximum)


        response_data['first_name']=first_name
        response_data['last_name']=last_name
        response_data['email_id']=email_id
        response_data['phone']=phone
        response_data['country_code']=country_code
        response_data['ev_desc']=ev_desc
        from django.http import JsonResponse
        return JsonResponse(response_data)
        
    else:
        response_data={}
        response_data['status']='Invalid'
        from django.http import JsonResponse
        return JsonResponse(response_data)
    
def ev_new_pwd(request):
    email=request.session['create_event_email_id']
    pwd_recieved=request.GET['pwd']
    country=request.session['create_event_country']
    state=request.session['create_event_state']
    city=request.session['create_event_city']
    event_category=request.session['create_event_event_category']
    event_sub_category=request.session['create_event_event_sub_category']
    heads=request.session['create_event_heads']
    ev_date=request.session['create_event_ev_date']
    budget=request.session['create_event_budget']
    first_name=request.session['create_event_first_name']
    last_name=request.session['create_event_last_name']
    email_id=request.session['create_event_email_id']
    phone=request.session['create_event_phone']
    country_code=request.session['create_event_country_code']
    ev_desc=request.session['create_event_ev_desc']

    user_login(fname=first_name,lname=last_name,Email=email,password=pwd_recieved,mobile_code=country_code,mobile=phone,country=country,state=state,city=city).save()


    event_category_name=event_categories.objects.get(id=event_category).category_name
    b=event_sub_category[1:-1]
    c=b.split(',')
    subcategories_data={}
    count=0
    for i in c:
        id=int(i[1:-1])
        sub_cat_name=event_sub_categories.objects.get(id=id).sub_category_name
        subcategories_data[int(count)]=sub_cat_name
        count+=1


    response_data={}

    import requests
    import json
    url = "https://api.countrystatecity.in/v1/countries/"+country

    headers = {
    'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    }

    response = requests.request("GET", url, headers=headers)

    data=response.text
    data_json=json.loads(data)
    response_data['status']='OK'
    response_data['country']=data_json['name']
    url = "https://api.countrystatecity.in/v1/countries/"+country+"/states/"+state
    response = requests.request("GET", url, headers=headers)

    data=response.text
    data_json=json.loads(data)
    response_data['state']=data_json['name']
    url = "https://api.countrystatecity.in/v1/countries/"+country+"/states/"+state+"/cities"
    response = requests.request("GET", url, headers=headers)
    data=response.text
    data_json=json.loads(data)
    count=0
    response_data['city']=''
    for i in range(0,len(data_json)):
        if data_json[i]['id'] == int(city):
            response_data['city']=data_json[i]['name']
            count+=1
            
    response_data['event_category']=event_category_name
    response_data['sub_category']=subcategories_data
    heads_data=event_heads_manager.objects.get(id=heads)

    response_data['heads']=str(heads_data.Minimum_Value)+' - '+str(heads_data.Maximum_Value)
    response_data['ev_date']=ev_date
    get_budget_data=event_budget_settings.objects.get(id=budget)
    user_country=Countries.objects.get(name=visitor_ip_address(request)).currency
    # import requests

    # # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+get_budget_data.country.currency

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()
    # onefcfa=float(data['conversion_rates'][str(user_country)])
    # ex_value=Exchange_Rates.objects.get(base_country=get_budget_data.country.currency,dest_country=user_country).ex_rate
    # onefcfa=float(ex_value)

    
    import requests

    url = 'https://api.exchangerate.host/convert?from='+get_budget_data.country.currency+'&to='+user_country
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])

    budget_minimum=round((get_budget_data.Minimum_Value)*(onefcfa),2)
    budget_maximum=round((get_budget_data.Maximum_Value)*(onefcfa),2)
    if user_country == 'XOF':
        user_country = 'F CFA'
    response_data['budget']=user_country+' '+str(budget_minimum)+' - '+user_country+' '+str(budget_maximum)

    response_data['first_name']=first_name
    response_data['last_name']=last_name
    response_data['email_id']=email_id
    response_data['phone']=phone
    response_data['country_code']=country_code
    response_data['ev_desc']=ev_desc
    from django.http import JsonResponse
    return JsonResponse(response_data)


def ev_data(request):
    email=request.session['create_event_email_id']
    pwd_recieved=request.GET['pwd']
    country=request.session['create_event_country']
    state=request.session['create_event_state']
    city=request.session['create_event_city']
    event_category=request.session['create_event_event_category']
    event_sub_category=request.session['create_event_event_sub_category']
    heads=request.session['create_event_heads']
    ev_date=request.session['create_event_ev_date']
    budget=request.session['create_event_budget']
    first_name=request.session['create_event_first_name']
    last_name=request.session['create_event_last_name']
    email_id=request.session['create_event_email_id']
    phone=request.session['create_event_phone']
    country_code=request.session['create_event_country_code']
    ev_desc=request.session['create_event_ev_desc']

    


    event_category_name=event_categories.objects.get(id=event_category).category_name
    b=event_sub_category[1:-1]
    c=b.split(',')
    subcategories_data={}
    count=0
    for i in c:
        id=int(i[1:-1])
        sub_cat_name=event_sub_categories.objects.get(id=id).sub_category_name
        subcategories_data[int(count)]=sub_cat_name
        count+=1


    response_data={}

    import requests
    import json
    url = "https://api.countrystatecity.in/v1/countries/"+country

    headers = {
    'X-CSCAPI-KEY': 'UktWSUFIa0VSazU1V1ZpZnRKN0IzNFVlWjRtWlR4bDl0Tm43RFcyNA=='
    }

    response = requests.request("GET", url, headers=headers)

    data=response.text
    data_json=json.loads(data)
    response_data['status']='OK'
    response_data['country']=data_json['name']
    url = "https://api.countrystatecity.in/v1/countries/"+country+"/states/"+state
    response = requests.request("GET", url, headers=headers)

    data=response.text
    data_json=json.loads(data)
    response_data['state']=data_json['name']
    url = "https://api.countrystatecity.in/v1/countries/"+country+"/states/"+state+"/cities"
    response = requests.request("GET", url, headers=headers)
    data=response.text
    data_json=json.loads(data)
    count=0
    response_data['city']=''
    for i in range(0,len(data_json)):
        if data_json[i]['id'] == int(city):
            response_data['city']=data_json[i]['name']
            count+=1
            
    response_data['event_category']=event_category_name
    response_data['sub_category']=subcategories_data
    heads_data=event_heads_manager.objects.get(id=heads)

    response_data['heads']=str(heads_data.Minimum_Value)+' - '+str(heads_data.Maximum_Value)
    response_data['ev_date']=ev_date
    get_budget_data=event_budget_settings.objects.get(id=budget)
    user_country=Countries.objects.get(name=visitor_ip_address(request)).currency
    # import requests

    # # Where USD is the base currency you want to use
    # url = 'https://v6.exchangerate-api.com/v6/ffb52277455f5c20a6f214d3/latest/'+get_budget_data.country.currency

    #     # Making our request
    # response = requests.get(url)
    # data = response.json()
    # onefcfa=float(data['conversion_rates'][str(user_country)])
    # ex_value=Exchange_Rates.objects.get(base_country=get_budget_data.country.currency,dest_country=user_country).ex_rate
    # onefcfa=float(ex_value)

    import requests

    url = 'https://api.exchangerate.host/convert?from='+get_budget_data.country.currency+'&to='+user_country
    response = requests.get(url)
    data = response.json()
    onefcfa=float(data['info']['rate'])
    budget_minimum=round((get_budget_data.Minimum_Value)*(onefcfa),2)
    budget_maximum=round((get_budget_data.Maximum_Value)*(onefcfa),2)

    if user_country == 'XOF':
        user_country = 'F CFA'

    response_data['budget']=str(budget_minimum)+' - '+str(budget_maximum)+' '+user_country

    response_data['first_name']=first_name
    response_data['last_name']=last_name
    response_data['email_id']=email_id
    response_data['phone']=phone
    response_data['country_code']=country_code
    response_data['ev_desc']=ev_desc
    from django.http import JsonResponse
    return JsonResponse(response_data)

def save_ev_data(request):
    vendor_type=request.GET['vendor_type']
    package_type=request.GET['package_type']
    ev_name=request.session['get_ev_name']
    country=request.session['create_event_country']
    state=request.session['create_event_state']
    city=request.session['create_event_city']
    event_category=request.session['create_event_event_category']
    event_sub_category=request.session['create_event_event_sub_category']
    heads=request.session['create_event_heads']
    ev_date=request.session['create_event_ev_date']
    budget=request.session['create_event_budget']
    first_name=request.session['create_event_first_name']
    last_name=request.session['create_event_last_name']
    email_id=request.session['create_event_email_id']
    phone=request.session['create_event_phone']
    country_code=request.session['create_event_country_code']
    ev_desc=request.session['create_event_ev_desc']
    request.session['user_login']=True
    request.session['user_email']=email_id

    vendor_type_json=vendor_type.split(',')
    import json

    aList = vendor_type_json
    jsonStr = json.dumps(aList)
    import uuid
    unique_id = uuid.uuid4()
    # pythonObj = json.loads(jsonStr)
    dict_obj={}
    for i in vendor_type_json:
        dict_obj[str(i)]='1'
        event_entries(Country=country,State=state,City=city,unique_id=unique_id,Event_Categories=event_category,Event_Sub_Categories=event_sub_category,Heads=heads,DOE=ev_date,Budget=event_budget_settings.objects.get(id=budget),First_Name=first_name,Last_Name=last_name,Email=email_id,MCode=country_code,Mobile=phone,Event_Desc=ev_desc,vendor_type=i,package_type=package_type,user_type=package_type,ev_name=ev_name,vendorjson=dict_obj).save()

    content=render_to_string('vendor_home/event_confirm.html')
    send_mail(subject='Congrats ! Your Event is Live |Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email_id], html_message=content)

    from django.core import serializers

    get_categories=vendor_type
    li = list(vendor_type_json)
    category_list_id=[]
    category_list=[]
    for i in li:
        if i == '':
            continue
        get_category_name=vendor_categories.objects.get(id=i).category_name
        category_list.append(get_category_name)
        category_list_id.append(i)

    # print(Convert(str1))
    # search_query_events=get_categories.replace('__#__',',')
    vendor_profile=Vendor_Users.objects.none()
    ven_list=''
    for i in category_list_id:
        ven_query = Vendor_Users.objects.filter(vendor_categories__has_key=str(i),is_otp_verified=True)
        ven_list=vendor_profile|ven_query
    # event_posted_1=event_entries.objects.filter(vendor_type__icontains='20')
    ven_list_list = ven_list.values_list('Email',flat=True)
    qs_json = serializers.serialize('json', ven_list.order_by('-created_on'))
    content=render_to_string('Mail_Contents/event_is_posted_vendor_notification_mail.html',)
    send_mail(subject='Another Event is Live | Eventinz - Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[ven_list_list], html_message=content)

    return HttpResponse("OK")

def update_user_profile(request):
    if request.method == 'POST':
        image_profile=request.FILES.get('image','')
        fname=request.POST['fname']
        lname=request.POST['lname']
        pwd=request.POST['pwd']
        user_id=request.POST['user_id']
        aboutme=request.POST['aboutme']
        db = user_login.objects.get(id=user_id)
        db.fname=fname
        db.lname=lname
        db.password=pwd
        db.aboutme=aboutme
        if image_profile == '':
            pass
        else:
            db.profile_image=image_profile
        db.save()
        return redirect('vendor_home:user_profile')


def about(request):
    content_about=EV_About.objects.get(id=1)
    content_teams=Eventinz_Teams.objects.all()
    context={
        "user_login1":request.session['user_login'],
        'content_about':content_about,
        'teams':content_teams,
        'is_french':request.session['is_french']

    }

    return render(request,'vendor_home/about.html',context)

def location_denied(request):
    return render(request,'vendor_home/error_location.html')

def get_email(request):
    from django.http import HttpResponse
    from django.http import JsonResponse
    from django.core import serializers


    import json
    id=request.GET['email']
    qs = user_login.objects.filter(Email=id)
    qs_json = serializers.serialize('json', qs)
    return HttpResponse(qs_json, content_type='application/json')

def user_send_otp(request):
    email=request.GET['email']
    request.session['fgt_email']=email
    
    fname=user_login.objects.get(Email=email).fname
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
        "OTP":random_str

    }
    return HttpResponse('DONE SENT')


def user_check_otp(request):
    sent_otp=request.session['forgot_otp']
    recieve_otp=request.GET['otp']
    if sent_otp == recieve_otp:
        return HttpResponse("OK")
    else:
        return HttpResponse("No")

def user_update_pwd(request):
    email=request.session['fgt_email']
    password=request.GET['password']

    db=user_login.objects.get(Email=email)
    db.password=password
    db.save()
    return HttpResponse('Done')

def close_event(request):
    id=request.GET['id']
    ev_db=event_entries.objects.get(id=id)
    ev_db.status='closed'
    ev_db.save()
    return redirect('vendor_home:my_events_all')

def cancel_event(request):
    id=request.GET['id']
    ev_db=event_entries.objects.get(id=id)
    ev_db.status='cancel'
    ev_db.save()
    return redirect('vendor_home:my_events_all')

def archieve_events(request):
    id=request.GET['id']
    ev_db=event_entries.objects.get(id=id)
    ev_db.is_archieve=True
    ev_db.save()
    return redirect('vendor_home:my_events_all')    


def unarchieve_events(request):
    id=request.GET['id']
    ev_db=event_entries.objects.get(id=id)
    ev_db.is_archieve=False
    ev_db.save()
    return redirect('vendor_home:my_events_all')    

def my_finance(request):
    return render(request,'user_profile/fin_dashboard.html')
def my_quotes(request):
    quotes=request_a_quote.objects.filter(email=request.session['user_email'])
    context={
        "quotes":quotes
    }
    return render(request,'user_profile/quotes.html',context)




def subscribe_newsletter(request):
    email=request.POST['emailid']
    url=request.POST['url']
    db = NewsLetter.objects.filter(email=email)
    if not db.exists():
        NewsLetter(email=email).save()
        context={
            'is_french':request.session['is_french'],
            'contact_details':EV_Contact.objects.get(id=1)
        }
        content=render_to_string('Mail_Contents/newsletter_subscribe.html',context)
        send_mail(subject='You Are Subscribed ! - Eventinz | Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content) 
    return redirect(url)

def exchange_rates_view(request):
    start_time=datetime.datetime.now()
    # Exchange_Rates.objects.all().delete()
    
    import requests
    import json
    import time
    # time.sleep(4)
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
                    )
                    if created:
                        obj.ex_rate=j
                        obj.save()
                    else:
                        obj.base_country=base_currency
                        obj.dest_country=i
                        obj.ex_rate=j
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
    return HttpResponse("OK")


def terms_and_conditions(request):
    data=Eventinz_Terms.objects.get(id=1)
    context={
        "data":data,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/tnc.html',context)

def privacy_policy(request):
    data=Eventinz_Privacy_Policy.objects.get(id=1)
    context={
        "data":data,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/tnc.html',context)

from django.core.serializers import serialize

def get_bank_acc_vendor(request):
    if request.method == "GET":
        id=request.GET['vid']
        bank_details=Vendor_bank_listing.objects.filter(Vendor_Id=id)
        data=serialize('json',bank_details)
        return HttpResponse(data,content_type="application/json")


def submit_transac_records(request):
    vendor_id=request.POST['vendor_id']
    quote_id=request.POST['quote_id']
    amount = float(request.POST['amount_pay'])
    host_email=request.session['user_email']
    host_id=user_login.objects.get(Email=host_email)
    pay_type=request.POST.get('pay_type')
    Bank_Name=request.POST['bank_name_user']
    Payment_By=''
    if Bank_Name == 'PayPal':
        Payment_By='PayPal'
    elif Bank_Name == 'MoMo':
        Payment_By = 'MoMo'
    else:
        Payment_By = 'MoMo'
    Account_Name=request.POST['acc_name_user']
    Bank_AC_Number=request.POST['acc_number_user']
    Country=request.POST['country_user']
    Bank_Reference_Code=request.POST['bank_ref_code']
    Depositor_Name=request.POST['depositor_name_user']
    vendor_id_object=Vendor_Users.objects.get(id=vendor_id)
    quote_id_object=request_a_quote.objects.get(id=quote_id)
    quote_id_object.status='Transaction Pending for Verification'
    quote_id_object.pay_num = '1'
    if pay_type == '2':
        quote_id_object.pay_num = '2'
        db = Vendor_Payment_History.objects.get(vendor_id=vendor_id,quote_id=quote_id,host_id=host_id.id).amount
        amount += db

    

    quote_id_object.save()
    Transaction_File_Record=request.FILES['transreciept']
    db=Vendor_Payment_History(vendor_id=vendor_id_object,quote_id=quote_id_object,host_id=host_id,Bank_Name=Bank_Name,Account_Name=Account_Name,Bank_AC_Number=Bank_AC_Number,Country=Country,Bank_Reference_Code=Bank_Reference_Code,Depositor_Name=Depositor_Name,Transaction_File_Record=Transaction_File_Record,Payment_By=Payment_By,amount = amount)
    db.save()
    content=render_to_string('Mail_Contents/milestone_recieved.html')
    send_mail(subject='Yayy ! You just recieved a Milestone Payment ! - Eventinz | Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[vendor_id_object.Email], html_message=content) 
    return redirect('vendor_home:user_profile')

def get_single_event(request,id):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        event_details=event_entries.objects.get(id=id)
        event_proposals=vendor_event_proposal.objects.filter(event_id=id)
        event_proposals_count=event_proposals.count()
        event_proposals_hired=vendor_event_proposal.objects.filter(event_id=id,status='Hired')
        
        country=get_user.country
        trans_history=Vendor_Payment_History_events.objects.filter(host_id=get_user.id,event_id=event_details.id)
        context={
            'user':get_user,
            'country':country,
            'location':visitor_ip_address(request),
            'event':event_details,
            'event_proposals':event_proposals,
            'event_proposals_hired':event_proposals_hired,
            'trans_history':trans_history,
            'event_proposals_count':event_proposals_count,
            'is_french':request.session['is_french'],
            
            
        }
        return render(request,'user_dashboard_v2/dashboard_events.html',context)

def get_single_event_review(request,id):
    if 'user_email' in request.session:
        user_email=request.session['user_email']
        get_user=user_login.objects.get(Email=user_email)
        event_details=event_entries.objects.get(id=id)
        event_proposals=vendor_event_proposal.objects.filter(event_id=id)
        event_proposals_count=event_proposals.count()
        event_proposals_hired=vendor_event_proposal.objects.filter(event_id=id,status='Hired')
        country=get_user.country
        trans_history=Vendor_Payment_History_events.objects.filter(host_id=get_user.id,event_id=event_details.id)


        reviews_to_vendor=event_reviews_user_to_vendor.objects.filter(event_id=id)
        review_allow=False
        review_db=''
        if reviews_to_vendor.exists():
            review_allow=False
            review_db=event_reviews_user_to_vendor.objects.get(event_id=id)
        else:
            review_allow=True
        context={
            'user':get_user,
            'country':country,
            'location':visitor_ip_address(request),
            'event':event_details,
            'event_proposals':event_proposals,
            'event_proposals_hired':event_proposals_hired,
            'trans_history':trans_history,
            'event_proposals_count':event_proposals_count,
            'review_allow':review_allow,
            'review_db':review_db,
            'is_french':request.session['is_french']
            
        }
        return render(request,'user_dashboard_v2/dashboard-rating.html',context)

def submit_review(request):
    event_id=request.POST['event_id']
    event_id_object=event_entries.objects.get(id=event_id)
    proposal_db_id = vendor_event_proposal.objects.get(event_id = event_id,status = "Hired").vendor_id

    url=request.POST['url']
    user=request.session['user_email']
    user_object=user_login.objects.get(Email=user)
    review_text=request.POST['review_text']
    review_star=request.POST['rating_star']
    event_reviews_user_to_vendor(event_id=event_id_object,review_from=user_object,review_text=review_text,review_star=review_star,vendor_id = proposal_db_id).save()
    return redirect(url)
def invoice_event(request):
    proposal_id=request.GET['proposal_id']
    vendor_event_proposal_data=vendor_event_proposal.objects.get(id=proposal_id)
    vendor_event_proposal_items_data=vendor_event_proposal_items.objects.filter(proposal_id=proposal_id)
    my_options=QRCodeOptions(size='m', border=6, error_correction='M')

    context={
        'vendor_event_proposal_data':vendor_event_proposal_data,
        'vendor_event_proposal_items':vendor_event_proposal_items_data,
        'my_options':my_options,
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french']
    }

    return render(request,'invoices/invoice-eventinz-event.html',context)

def hire_event_vendor(request):
    id=request.GET['eid']
    pid=request.GET['pid']
    db=event_entries.objects.get(id=id)
    db.status='Hired'
    db1=vendor_event_proposal.objects.get(id=pid)
    vendor_mail = db1.vendor_id.Email
    db1.status='Hired'
    db.save()
    db1.save()
    order_db=total_accepted_orders.objects.get(vendor_id=db1.vendor_id.id)
    order_db.order_count+=1
    order_db.save()
    monthly_graph = total_sales.objects.get(vendor_id=db1.vendor_id.Email)
    from datetime import datetime
  
    today = datetime.now()
    month = today.month
    if month == 1:
        monthly_graph.Jan_sales+=1
    if month == 2:
        monthly_graph.Feb_sales+=1
    if month == 3:
        monthly_graph.Mar_sales+=1
    if month == 4:
        monthly_graph.Apr_sales+=1
    if month == 5:
        monthly_graph.May_sales+=1
    if month == 6:
        monthly_graph.Jun_sales+=1
    if month == 7:
        monthly_graph.Jul_sales+=1
    if month == 8:
        monthly_graph.Aug_sales+=1
    if month == 9 :
        monthly_graph.Sep_sales+=1
    if month == 10:
        monthly_graph.Oct_sales+=1
    if month == 11:
        monthly_graph.Nov_sales+=1
    if month == 12:
        monthly_graph.Dec_sales+=1
    monthly_graph.save()
    mail_data = {
        'company_name':db1.vendor_id.Company_Name
    }
    content=render_to_string('Mail_Contents/hire_event_vendor_mail.html', mail_data)
    send_mail(subject='You Are Hired !! - Eventinz | Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[vendor_mail], html_message=content) 
    return redirect('vendor_home:my_events_all')

def save_event_transaction(request):
    vendor_id=request.POST['vendor_id']
    event_id=request.POST['event_id']
    host_email=request.session['user_email']
    bank_name=request.POST['bank_name']
    account_name=request.POST['account_name']
    transac_file=request.FILES['transreciept']
    amount=request.POST['amount']
    account_num=request.POST['acc_num']
    vendor_id_object = Vendor_Users.objects.get(id=vendor_id)
    event_id_object =  event_entries.objects.get(id=event_id)
    host_email_object = user_login.objects.get(Email=host_email)

    Vendor_Payment_History_events(vendor_id=vendor_id_object,event_id=event_id_object,host_id=host_email_object,Bank_Name=bank_name,Account_Name=account_name,Transaction_File_Record=transac_file,Bank_AC_Number=account_num,Amount=amount).save()
    return redirect('vendor_home:my_events_all')
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def do_momo_tran(request):
    from . import momotran

    amount = request.GET['amount']
    mobile = '229'+str(request.GET['mobile'])
    currency = request.GET['currency']

    # momotran.main_call(amount,mobile,currency)
    payment = momotran.main_call_live(amount,mobile,currency)

    if payment == False:
        return HttpResponse("Payment Status is False")
    elif payment == True:
        return HttpResponse("OK")
    else:
        return HttpResponse(payment)

    # return HttpResponse("OK")

@csrf_exempt
def do_moove_tran(request):
    from . import moove_api

    amount = request.GET['amount']
    mobile = '229'+str(request.GET['mobile'])
    currency = request.GET['currency']

    payment = moove_api.moove_main_call(amount=amount,mobile=mobile)

    if payment == "SUCCESS":
        return HttpResponse("OK")
    else:
        return HttpResponse(payment)

def my_ev_support(request):
    faq = Vendor_FAQ.objects.filter(status = 'active').order_by('created_at')
    context = {
        'faq':faq,
        'is_french':request.session['is_french']
    }
    return render(request,'user_dashboard_v2/ev_chat.html',context)


def close_ev(request,id):
    db=event_entries.objects.get(id=id)
    db.status = 'Complete'
    db.save()
    return redirect('vendor_home:my_events_all')

def setlang(request):
    is_french=request.GET['active']
    request.session['is_french']=is_french
    return HttpResponse("Done")

def check_user_pwd(request):
    user_id=request.session['user_email']
    pwd = request.GET['pwd']
    db = user_login.objects.get(Email = user_id)
    cp = db.password
    if cp == pwd:
        return HttpResponse("OK")
    else:
        return HttpResponse("NO")

def resend_otp_event(request):
    email = request.session['create_event_email_id']
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
    
    otp=random_str
    request.session['create_event_otp']=otp
    content=render_to_string('vendor_home/event_otp.html',{'otp':otp})
    send_mail(subject='Authenticate via OTP - Eventinz | Your Event Your Way', message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
    return HttpResponse("OK")

def contact(request):
    data = EV_Contact.objects.get(id=1)
    context={
        'data':data,
        'is_french':request.session['is_french']
    }
    return render(request,'vendor_home/ev_contact.html',context)

def my_chat_view(request):
    user_email = request.session['user_email']
    vendor_proposal_hired = vendor_event_proposal.objects.filter(event_id__Email=request.session['user_email'],status='Hired')
    total_event=event_entries.objects.filter(Email=user_email)
    total_event_count=total_event.count()
    ongoing_event=event_entries.objects.filter(Email=user_email,status='Hired')
    ongoing_event_count=ongoing_event.count()
    complete_event=event_entries.objects.filter(Email=user_email,status="Complete")
    complete_event_count=complete_event.count()
    cancel_event=event_entries.objects.filter(Email=user_email,status="cancel")
    cancel_event_count=cancel_event.count()
    context = {
        "vendor_hired":vendor_proposal_hired,
        'events':total_event,
        'event_count':total_event_count,
        'ongoing_event_count':ongoing_event_count,
        "complete_event_count":complete_event_count,
        'get_user_location':visitor_ip_address(request),
        'is_french':request.session['is_french'],
        'cancel_event_count':cancel_event_count
    }
    return render(request,'user_dashboard_v2/chat_view.html',context)


def vendor_public_profile(request,id,name):
    vendor_profile = Vendor_Users.objects.get(id=id)
    context = {
        'vendor_profile':vendor_profile
    }
    return HttpResponse("OK")



def statistics(request):
    context={
        'is_french':request.session['is_french']
    }
    return render(request,"user_dashboard_v2/dashboard_user_page.html",context)

def all_packages(request):
    import math
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    

    packages = vendor_public_packages.objects.filter().distinct('package_name')
    
    Page = Paginator(packages,50)
    page_number = request.GET.get('page')
    try:
        page_obj = Page.page(page_number)
    except PageNotAnInteger:
        page_obj = Page.page(1)
    except EmptyPage:
        page_obj = Page.page(Page.num_pages)
    
    if 'user_location_track' in request.session:

        location=request.session['user_location_track']
    else:
        location = visitor_ip_address(request)
    package_page_cms= Packages_CMS.objects.get(id=1)
    context = {
        'package_page':package_page_cms,
        'packages':page_obj,
        'get_user_location':location,
        'is_french':request.session['is_french'],
        "user_login1":request.session['user_login'],

    }
    return render(request,"vendor_home/package_page.html",context)


def send_moove_request(request):
    import requests

    url = "https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"

    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\r\n<S:Envelope xmlns:S=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n    <SOAP-ENV:Header/>\r\n    <S:Body>\r\n        <ns2:Push xmlns:ns2=\"http://api.merchant.tlc.com/\">\r\n            <token>5x6HzkGQz9cBfj6eO3n/rG0alcD8rIkXwWWBzl67LnwMhReWihY9SNcHXEX2H4r4</token>\r\n            <msisdn>22995938063</msisdn>\r\n            <message>TEST</message>\r\n            <amount>100</amount>\r\n            <externaldata1>22995000355</externaldata1>\r\n            <fee>0</fee>\r\n        </ns2:Push>\r\n    </S:Body>\r\n</S:Envelope>"
    headers = {
    'Content-Type': 'text/xml; charset=utf-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    import xmltodict, json
    obj = xmltodict.parse(response.text)
    obj_json = json.dumps(obj)
    # print(response.text)
    return HttpResponse(obj_json)


def check_moove_request(request):
    import requests

    reqUrl = "https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/xml" 
    }

    payload = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="http://api.merchant.tlc.com/">\n <soapenv:Header/>\n <soapenv:Body>\n <api:getMobileAccountStatus>\n <!--Optional:-->\n <token>5x6HzkGQz9cBfj6eO3n/rG0alcD8rIkXwWWBzl67LnwMhReWihY9SNcHXEX2H4r4</token>\n <!--Optional:-->\n <request>\n <!--Optional:-->\n <msisdn>22995938063</msisdn>\n </request>\n </api:getMobileAccountStatus>\n </soapenv:Body>\n</soapenv:Envelope>'

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList,verify=False)

    import xmltodict, json
    obj = xmltodict.parse(response.text)
    obj_json = json.dumps(obj)
    # print(response.text)
    return JsonResponse(obj)


def checkMooveTransaction(request):
    import requests,xmltodict,json
    transID = "20086B3B-E229-4130-91BA-D0039405044D"
    reqUrl = "https://testapimarchand2.moov-africa.bj:2010/com.tlc.merchant.api/UssdPush?wsdl"

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
    return HttpResponse(str(status))



def userSignUp(request):
    modal_active=False

    
    if request.method=='POST':
        get_url=request.POST['geturl']

        form=MyForm(request.POST)
        
        if form.is_valid():
            fname=request.POST['fname']
            lname=request.POST['lname']
            email=request.POST['email']
            mno_code=request.POST['mno_code']
            mobile=request.POST['mobile']
            password=request.POST['password']
            re_password=request.POST['re_password']
            countries=request.POST['countries']
            state=request.POST['state']
            city=request.POST['city']
            if (password==re_password):
                check_db = user_login.objects.filter(Email=email)
                if not check_db.exists():

                    user_login(fname=fname,lname=lname,Email=email,password=password,mobile_code=mno_code,mobile=mobile,country=countries,state=state,city=city).save()
                    request.session['user_login']=True
                    request.session['user_email']=email
                    get_mail_db=User_Welcome_Mail.objects.get(id=1)
                # send_mail(
                #     'activation mail',
                #     'message here',
                #     'support@eventinz.com',
                #     [email],
                #     fail_silently=False,
                #     )

                    mail_context={
                        'data':get_mail_db,
                        'fname':fname,
                        'is_french':request.session['is_french']
                    }
                    content=render_to_string('vendor_home/mail_welcome.html',mail_context)
                    send_mail(subject=get_mail_db.subject, message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)
                
                return redirect(get_url)
                # messages.info(request,"password matched")

            else:
                messages.info(request,"password not match")
                return redirect(get_url)

                
            # print("success")
        else:
            modal_active=True
            messages.info(request,"captcha invalid")
            return redirect(get_url)

