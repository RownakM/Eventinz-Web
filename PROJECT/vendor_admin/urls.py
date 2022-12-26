from django.urls import path,include

from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.main_home,name='vendor_home'),
    
    path('dashboard/', views.index, name='vendor_index'),
    path('login/',views.login,name='vendor_login'),
    path('profile/',views.profile,name='vendor_profile'),
    path('profile/edit/',views.profile_update,name="vendor_profile_update"),
    path('register/',views.signup,name='vendor_signup'),
    path('auth/',views.auth,name='vendor_auth'),
    path('auth/resend/',views.resend_otp_vendor_reg,name="resend_otp_vendor_reg"),
    path('verify/',views.auth_verify,name='vendor_auth_otp'),
    path('pricing/',views.pricing,name='vendor_pricing'),
    path('renewal/',views.pricing_renewal,name="pricing_renewal"),
    path('logout/',views.logout,name="vendor_logout"),
    path('payments/',views.payment,name="vendor_payment_page"),
    path('renewal/session/',views.payment_session_update,name="payment_session_update"),
    path('renewal/payments/',views.payment_renew,name="vendor_payment_renew"),
    path('active-events/',views.active_events,name="active_events"),
    path('payment/',views.payment_session,name="payment_session"),
    path('payments/',views.checkout_session,name="vendor_checkout_session"),
    path('renewal/payments/session/',views.checkout_session_renewal,name="checkout_session_renewal"),

    path('checkout/',views.checkout,name="Vendor_Checkout"),
    path('renewal/checkout/',views.checkout_renewal,name="Vendor_Checkout_renewal"),

    path('payments/success/',views.payment_success,name="vendor_payment_success"),
    path('invoice/',views.invoice,name="Vendor_invoice"),
    path('get-state/',views.get_state,name="Get_State"),
    path('get-email/',views.get_email,name="Get_Email"),
    path('otp/',views.otp,name='verify_otp'),
    path('google-auth-success/',views.google_auth_success,name="google_auth_success"),
    path('vendor-profile-update/',views.vendor_update_profile,name="update_on_post"),
    # path('set-session/',views.check_user_or_vendor,name="UoV"),
    path('test-google/',views.test_google),
    # path('my-deals/',views.my_deals,name="vendor_my_deals"),
    # path('my-deals/delete/<str:id>/',views.my_deals_delete,name="vendor_my_deals"),

    # path('my-deals/create/',views.my_deals_create,name="vendor_my_deals_create"),

    # path('save_deals/',views.save_deals,name="save_deals"),
    path('chat/',include('chat.urls')),
    path('my-chats/<str:quote_id>/',views.my_chat,name="My_Chat"),
    path('my-chats/<str:quote_id>/events/',views.my_chat_events,name="My_Chat_events"),

    path('my-chats/',views.my_chat_dup,name="chat_dup_ven"),
    path('chatroom/',views.chatroom,name="Chatroom"),
    path('chatroom/live/',views.chat_live,name="Chat_live") ,
    path('my-packages/',views.my_packages,name="My_Packages"),
    path('my-packages/all/',views.my_packages_view,name="my_packages_view"),
    path('my-packages/<str:name>/view/',views.my_packages_view_single,name="my_packages_view_single"),

    path('my-packages/<str:id>/edit/',views.my_packages_edit,name="my_packages_edit"),

    path('get-sub-cat/',views.get_sub_categories,name="get_sub_cat"),
    path('my-listings/',views.my_listings,name="my_listings"),
    path('my-packages-post/',views.my_packages_on_post,name="my_packages_post"),
    path('my-packages-edit/',views.my_packages_edit_on_post,name="my_packages_edit_on_post"),
    path('my-packages/delete/<str:id>/',views.my_packages_delete,name="my_packages_delete"),


    path('my-gallery/',views.my_gallery,name="my_gallery"),
    path('my-gallery/create/',views.my_gallery_create,name="my_gallery_create"),
    path('my-gallery/delete/<str:id>/',views.my_gallery_delete,name="my_gallery_delete"),


    path('my_gallery_post',views.my_gallery_post,name="my_gallery_post"),
    path('my-quote-request',views.my_quote_request,name="my_quote_request"),
    path('get-content',views.get_content,name="get_content"),
    path('quote_states/',views.quote_states,name="change_quote_state"),
    path('billing/',views.billing,name="vendor_billing"),
    path('get_quote_details/',views.get_quote_details,name="get_quote_details"),
    path('bill_items/',views.bill_items,name="items_bill"),
    path('request_rem_amt/',views.request_rem_amt,name="request_rem_amt"),
    path('vendor_send_otp/',views.vendor_send_otp,name="vendor_send_otp"),
    path('vendor_check_otp/',views.vendor_check_otp,name="vendor_check_otp"),
    path('vendor_update_pwd/',views.vendor_update_pwd,name="vendor_update_pwd"),
    path('get_live_events/',views.get_live_events,name="get_live_events"),
    path('get_event_categories/',views.get_event_categories,name="get_event_categories"),
    path('get_vendor_categories/',views.get_vendor_categories,name="get_vendor_categories"),



    path('events/',views.event_live,name="event_live"),
    path('events/<str:id>/',views.event_live_details,name="event_live_details"),
    path('events/<str:id>/<str:proposal_id>/edit/',views.event_live_details_edit,name="event_live_details_edit"),


    path('save_events_proposal/',views.save_event_proposal,name="save_event_proposal"),
    path('save_events_proposal_update/',views.save_event_proposal_update,name="save_event_proposal_update"),

    path('event-transactions/',views.event_transactions,name="event_transactions"),
    path('quote-transactions/',views.proposal_transactions,name="proposal_transactions"),

    path('quote_pay_confirm/',views.quote_pay_confirm,name="quote_pay_confirm"),

    path('my-proposals/',views.my_proposals,name="my_proposals"),
    path('my-bank/',views.my_bank,name="my_bank"),
    path('add-bank-post/',views.my_bank_add,name="bank_on_post"),
    path('accept_trans/',views.accept_trans,name="accept_trans1"),
    path('reject_trans/',views.reject_trans,name="reject_trans1"),



    path('accept_trans/<str:id>/',views.accept_trans,name="accept_trans"),
    path('reject_trans/<str:id>/',views.reject_trans,name="reject_trans"),
    path('renew-leads/',views.renew_leads,name="renew_leads"),
    path('renew_leads_momo/',views.renew_leads_momo,name="renew_leads_momo"),
    path('renew_leads_paypal/',views.renew_leads_paypal,name="renew_leads_paypal")


    
    
    

    
    

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
