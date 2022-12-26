'''PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # path('grappelli/', include('grappelli.urls')), # grappelli URLS
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('jet/', include('jet.urls', 'jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('eventinz-admin/dashboard/', admin.site.urls),
    # path('ojuelegba12/admin-tools/',include('admin_tools.urls')),
    path('', include('helloworld.urls')),
    # path('',include('vendor_home.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('vendor/',include('vendor_admin.urls')),
    path('staging/',include('vendor_home.urls')),
    path('fr/',include('vendor_home_french.urls')),
    path('paypal/', include('base.urls')),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('u/dashboard/',include('user_dashboard.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('captcha/',include("captcha.urls")),
    path('chat/',include('chat.urls')),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
