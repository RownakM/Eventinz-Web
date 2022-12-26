from django.shortcuts import render, redirect
from .models import Room, Message
from vendor_admin.models import Vendor_Users
from user_dashboard.models import user_login
from django.http import HttpResponse, JsonResponse

def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username') # henry
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {

        'username': username,
        'room': room,
        'room_details': room_details,
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect(room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect(room+'/?username='+username)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    quote_id=request.POST['quote_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    # return HttpResponse("Hi, Message Sent Successfully!!")

def getMessages(request,  room,quote_id):
    room_details = Room.objects.get(name=room,quote_id=quote_id)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})

from django.db.models import Q

def checkmessages(request,room,quote_id):
    room_details = Room.objects.get(name=room,quote_id=quote_id)
    import datetime
    a = datetime.now()
    b = a - datetime.timedelta(seconds = 1) # days, seconds, then other fields.

    messages = Message.objects.filter(room=room_details.id,created_on = b).exclude(user = request.session['vendor_email'])
    if messages.exists():
        return HttpResponse("Yes")
    else:
        return HttpResponse("No")


def checkmessage(request,ven_id):
    room_details = Room.objects.all()
    import datetime
    a = datetime.datetime.now()
    b = a - datetime.timedelta(seconds = 10) # days, seconds, then other fields.
    vendor_profile = Vendor_Users.objects.get(id=ven_id)
    response = False
    for room in room_details:

        messages = Message.objects.filter(room=room.id,created_on__gt=b).exclude(user = vendor_profile.Company_Name)
        if messages.exists():
           response = 'Yes'
           break
            
        else:
            response = 'No'
            continue
    return HttpResponse(response)
    

def checkUserMessage(request,user_id):
    room_details = Room.objects.all()
    import datetime
    a = datetime.datetime.now()
    b = a - datetime.timedelta(seconds = 10) # days, seconds, then other fields.
    vendor_profile = user_login.objects.get(id=user_id)
    response = False
    for room in room_details:
        messages = Message.objects.filter(room=room.id,created_on__gt=b).exclude(user = vendor_profile.fname)
        if messages.exists():
           response = 'Yes'
           break
            
        else:
            response = 'No'
            continue
    return HttpResponse(response)