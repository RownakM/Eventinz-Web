import datetime
from email.quoprimime import quote
import math
import random
import re
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from urllib3 import HTTPResponse
from Eventinz_Terms_And_Conditions.models import Eventinz_Privacy_Policy, Eventinz_Terms
from Mails.models import User_Welcome_Mail
from about.models import EV_About, Eventinz_Teams
from eventmanager.models import create_event_packages, event_budget_settings, event_entries, event_heads_manager, event_planner_CMS, event_reviews_user_to_vendor, vendor_event_proposal, vendor_event_proposal_items
from helloworld.models import NewsLetter

from transaction_records_user.models import Vendor_Payment_History, Vendor_Payment_History_events, user_transaction_records
from vendor_home.forms import MyForm
from user_dashboard.models import user_login
# Create your views here.
from indexCMS.models import Vendor_Categories_Text, Vendor_Deals_Index_CMS, advertisement, how_eventinz_works, index_slider,index_headers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from content_app.models import Exchange_Rates, Exchange_Rates_API, Our_Vendor_CMS, Venue_Type_by_venue, Venue_main_home, cron_activities, event_categories,event_categories_french,event_sub_categories,event_sub_categories_french,Venue_Type,Venue_Details
from vendor_admin.models import Countries, Vendor_Users, Vendor_bank_listing, request_a_quote, search_cms, total_sales, total_sales_count, vendor_categories, vendor_gallery, vendor_packages, vendor_public_deals, vendor_public_packages, vendor_quote_invoice,vendor_sub_categories, vendor_subscription
from blogs.models import Blog_Category_Details, Post,blog_category,Blog_CMS,PostImage
from django.db.models import Subquery
from chat.models import Room, Message


def visitor_ip_address(request):

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
                content=render_to_string('vendor_home/mail_welcome.html',{'data':get_mail_db,'fname':fname})
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
        'deals':deals


    }
    return render(request,'vendor_home/index.html',context)