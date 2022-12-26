from django.urls import path

from . import views
app_name='vendor_home'
urlpatterns = [

    path('', views.index, name='vendor_home_index'),
    path('create_user/',views.userSignUp,name="user_signUp"),
    path('/v-<str:id>/<str:name>/',views.vendor_public_profile,name="vendor_public_profile"),
    path('blogs/',views.blogs,name='vendor_blog'),
    path('contact-us/',views.contact,name="vendor_contact"),
    path('inner/',views.inner_page,name='vendor_inner'),
    path('test/',views.test,name="test"),
    path('get-sub-cat/',views.get_sub_categories,name="get_sub_cat"),
    path('get-sub-cat-vendor/',views.get_sub_category_vendor,name="get_sub_cat_vendor"),

    path('get-email/',views.get_email,name="Get_User_Email"),
    path('blogs/<str:id>/<str:name>/',views.get_blog_detail,name="blog_single"),
    path('blogs/category/<str:id>/<str:name>/',views.get_blog_content_page,name="blog_content_page"),

    path('venues/<str:venue_type>/',views.get_venue,name="all_venue"),
    
    path('venues/',views.get_venues,name='Venue'),
    path('venues/<str:venue_type>/<str:list_id>/<str:title>/',views.get_single_venue,name="s_venue"),
    path('track-me/<str:lon>/<str:lat>/',views.get_location,name="track_me"),
    path('track-me/',views.get_location_new,name="track_me_new"),
    # path('deals/',views.deals,name="deals"),
    path('about/',views.about,name="about"),
    path('vendor_request_on_post/',views.request_quote,name="request_quote"),
    path('user_login/',views.user_login_view,name="user_login_url"),
    path('profile/',views.user_profile,name="user_profile"),
    path('support/',views.my_ev_support,name="my_ev_support"),
    path('statistics/',views.statistics,name="user_statistics"),
    path('profile/events/<int:id>/',views.get_single_event,name="get_single_event"),
    path('profile/events/<int:id>/review/',views.get_single_event_review,name="get_single_event_review"),
    path('profile/get_submit/',views.submit_review,name="submit_review"),

    path('profile/events/all/',views.my_events_all,name="my_events_all"),
    path('profile/events/archieve/',views.my_events_all_unarchieve,name="my_events_all_unarchieve"),
    path('profile/events/open/',views.my_events_open,name="my_events_open"),
    path('profile/events/closed/',views.my_events_closed,name="my_events_closed"),
    path('profile/events/progress/',views.my_events_progress,name="my_events_progress"),
    path('profile/events_close/<str:id>/',views.close_ev,name="close_ev"),

    path('close_event/',views.close_event,name="close_event"),
    path('cancel_event/',views.cancel_event,name="cancel_event"),
    path('archieve_event/',views.archieve_events,name="archieve_events"),
    path('unarchieve_event/',views.unarchieve_events,name="unarchieve_events"),

    # path('profile/my-transactions/',views.my_transactions,name="my_transaction"),
    path('locate/',views.visitor_ip_address,name="visitor_ip_address"),
    path('hire_event_vendor/',views.hire_event_vendor,name="hire_event_vendor"),
    path('invoice/',views.invoice,name="user_invoice"),
    path('invoice_event/',views.invoice_event,name="event_invoice"),
    path('chat/<str:quote_id>/',views.user_chat,name="user_chat"),

    path('chat/<str:event_id>/events/',views.user_chat_events,name="user_chat_events"),
    path('chat/',views.chat_dup,name="chat_dup"),
    path('create-event/',views.create_event,name="create_event"),
    path('create-event/resend-otp/',views.resend_otp_event,name="create_event_resend"),
    path('accept-quote/',views.accept_quote,name="accept_quote"),
    path('reject-quote/',views.reject_quote,name="reject_quote"),
    path('save_transaction/',views.save_transaction_record,name="save_transaction"),
    path('save_transaction_events/',views.save_event_transaction,name="save_transaction_event"),

    path('event-planners/',views.events,name="events"),
    path('event-planners/<str:venue_type>/',views.get_event_planners,name="all_event_planners"),
    path('get-email/',views.get_email,name="userGet_Email"),
    path('user_send_otp/',views.user_send_otp,name="user_send_otp"),
    path('user_check_otp/',views.user_check_otp,name="user_check_otp"),
    path('user_update_pwd/',views.user_update_pwd,name="user_update_pwd"),
    
    path('our-vendors/',views.our_vendors,name="our_vendors"),
    path('our-vendors/<str:type_vendor>/',views.get_vendor,name="our_vendors_pages"),
    path('our-vendors/<str:type_vendor>/<str:event_type>/',views.get_vendor_url,name="get_vendor_url"),
    path('our-vendors/<str:type_vendor>/<str:event_type>/<str:id_vendor>/<str:name_vendor>/',views.get_vendor_profile,name="get_vendor_profile"),
    path('search/',views.vendor_search,name="vendor_search"),
    path('search/<str:id_vendor>/<str:name_vendor>/',views.get_vendor_profile_search,name="vendor_profile_search"),
    path('logout/',views.user_profile_logout,name="user_profile_logout"),
    path('get_event_sub_cat/',views.get_event_sub_cat,name="get_event_sub_cat"),
    path('ev_send_mail/',views.ev_send_mail,name="ev_send_mail"),
    path('ev_check_otp/',views.ev_check_otp,name="ev_check_otp"),
    path('ev_check_pwd/',views.ev_check_pwd,name="ev_check_pwd"),
    path('ev_new_pwd/',views.ev_new_pwd,name="ev_new_pwd"),
    path('ev_data',views.ev_data,name="ev_data"),
    path('save_ev_data',views.save_ev_data,name='save_ev_data'),
    path('update_user_profile/',views.update_user_profile,name='update_user_profile'),
    path('location-denied/',views.location_denied,name="location_denied"),


    path('my-finance/',views.my_finance,name="my_finance"),
    path('my-quotes/',views.my_quotes,name="my_quotes"),


    path('subscribe-newsletter/',views.subscribe_newsletter,name="subscribe_newsletter"),
    path('exchange-rates/',views.exchange_rates_view,name="xchange_rates"),
    path('terms-and-conditions/',views.terms_and_conditions,name="termsncond"),
    path('privacy-policy/',views.privacy_policy,name="privacynpolicy"),

    path('get_bank_acc_vendor/',views.get_bank_acc_vendor,name="get_bank_acc_vendor"),

    path('submit_transac_records/',views.submit_transac_records,name="submit_transac_records"),
    path('momo_pay_event/',views.do_momo_tran,name="momo_event"),
    path('moove_pay_event/',views.do_moove_tran,name="moove_event"),
    path('set_lang/',views.setlang,name="set_lang"),
    path('check_user_pass/',views.check_user_pwd,name="check_user_pwd"),


  
    path('my-chats/',views.my_chat_view,name="my_chat_view"),

    path('packages/',views.all_packages,name="all_packages"),

    path('send_request/',views.send_moove_request,name="smvrqst"),
    path('check_request/',views.check_moove_request,name="cmvrst"),
    path('check_trans/',views.checkMooveTransaction,name="ctrans")
    

]