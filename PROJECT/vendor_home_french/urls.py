from django.urls import path

from . import views
app_name='vendor_home_french'

urlpatterns = [
    path('', views.index, name='vendor_home_index'),

]