from asyncio import FastChildWatcher
from django.conf import Settings
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import Group
from helloworld.models import Entries, Header,Mail_User,Mail_Vendor
from django.template.loader import render_to_string

from helloworld.models import About

def index(request):
    sub_status=False
    problem=False
    problem_id=None
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        mobile=request.POST['mobile']
        a=0
        typ=request.POST['type']
        country=request.POST['country']
        if(country=='Nigeria'):
            mobile='+234 '+str(mobile)
        elif(country=='Ivory Coast'):
            mobile='+225 '+str(mobile)
        elif(country=='Benin'):
            mobile='+229 '+str(mobile)
        
        if(Entries.objects.filter(email=email).exists()):
            problem=True
            problem_id='Email'
        if(Entries.objects.filter(mobile=mobile).exists()):
            problem=True
            problem_id='Mobile'
        else:
            form = Entries(fname=fname,lname=lname,email=email,mobile=mobile,User_Type=typ,country=country)
            form.save()
            sub_status=True
        body=''
        subject=''
        if(typ=='Vendor'):
            body=Mail_Vendor.objects.get().content
            subject=Mail_Vendor.objects.get().subject
        elif(typ=='User'):
            body=Mail_User.objects.get().content
            subject=Mail_User.objects.get().subject
            content=render_to_string('comingsoon/mail.html', {'i': body})
            send_mail(subject=subject, message=content, from_email='support@eventinz.com', recipient_list=[email], html_message=content)

        # g = Group.objects.get(name='mail_group_vendors')
        # users = Entries.objects.all()
        # for u in users:
        #     g.user_set.add(u)
            # return redirect('home')
    
    # return HttpResponse("Hello, world.")
    about=About.objects.all()
    Hea_img=Header.objects.get().image
    Text=Header.objects.get().Heading
    Button=Header.objects.get().button_text
    context={
        "about":about,
        "status":sub_status,
        'Header':Hea_img,
        "Text":Text,
        "Btext":Button,
        "problem":problem,
        "problem_id":problem_id
    }
    return render(request,'comingsoon/index-particles.html',context)

