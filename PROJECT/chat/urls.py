from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name="checkview"),
    path('send', views.send, name="send"),
    path('getMessages/<str:room>/<str:quote_id>/', views.getMessages, name="getMessages"),
    path('checkmessages/check/<str:ven_id>/',views.checkmessage, name="checkmessage"),
    path('checkusermessages/check/<str:user_id>/',views.checkUserMessage, name="checkUsermessage")


]