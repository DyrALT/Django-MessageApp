from typing import SupportsIndex
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout as logout_, login as login_
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, message,send_mail
from django.contrib.auth.models import User
from django.views.generic import View
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from .models import Message, Room
from django.utils import timezone

@login_required(login_url="login")
def index(request):
    users=User.objects.all().exclude(username=request.user.username)
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    return render(request, 'index.html',{"users":users})
@login_required(login_url="login")
def room(request, room_name):
    rooom = Room.objects.get(id=room_name)
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    if rooom.first_user == request.user or rooom.second_user == request.user:   
        users=User.objects.all().exclude(username=request.user.username)
        room=Room.objects.get(id=room_name)
        messages=Message.objects.filter(room=room)
        return render(request, 'room_v2.html', {
            'room_name': room_name,
            "users":users,
            "room":room,
            "messages":messages
        })
    else:
        return redirect("index")
@login_required(login_url="login")

def start_chat(request,id):
    second_user=User.objects.get(id=id)
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    try:
        room=Room.objects.get(first_user=request.user,second_user=second_user)
        return redirect("room",room.id)
    except Room.DoesNotExist:
        try:
            room=Room.objects.get(second_user=request.user,first_user=second_user)
            return redirect("room",room.id)
        except Room.DoesNotExist:
            room=Room.objects.create(first_user=request.user,second_user=second_user)
            return redirect("room",room.id)

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email,password=password)
        if user is not None:
            login_(request,user)
            return redirect("index")
        user = authenticate(username=email,password=password)
        if user is not None:
            login_(request,user)
            return redirect("index")
        messages.info(request,"Kullanıcı Adı Veya Şifre Hatalı")
        return render(request,"login.html")
    return render(request,"login.html")

def logout(request):
    User.objects.filter(id=request.user.id).update(last_login=timezone.now())
    logout_(request)
    return redirect("login")
    
def register(request):
    if request.method == "POST":
    
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        e_mail = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        username = f"{firstname} {lastname}"
        if password != confirm:
            messages.info(request,"Şifreler Eşleşmiyor")
            return redirect("register")
        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=e_mail).exists():
            if len(password) < 8:
                messages.info(request,"Şifre En az 8 karakter olmalıdır")
                return redirect("register")
            user = User.objects.create_user(username=username,email=e_mail,first_name=firstname,last_name=lastname)
            user.set_password(password)
            user.is_active = False
            user.save()
            uidb64 =  urlsafe_base64_encode(force_bytes(user.pk))
            domain=get_current_site(request).domain
            link=reverse('confirm',kwargs={'uidb64':uidb64,"token":token_generator.make_token(user)})
            activate_url="http://"+domain+link
            subject = "E-postanızı Doğrulayın"
            content = f"Sayın {username} doğrulama linkiniz: {activate_url} \nLütfen kimseyle paylaşmayınız.\n\nVatzap"
            email = send_mail(subject=subject,message=content,recipient_list=[e_mail],from_email="django.mail.backend@gmail.com",fail_silently=False)
            # login_(request,user)
            context = {
                "e_mail" : e_mail,

            }
            messages.success(request,"Başarıyla Kayıt Oldunuz")
            return render(request,"email_confirm.html",context)
        messages.info(request,"Kullanıcı Zaten Mevcut")
        return redirect("register")
        
    return render(request,"register.html")

class VerifacationsView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if user.is_active:
                login_(request,user)
                return redirect("index")
            user.is_active = True
            user.save()
            login_(request,user)
            return redirect("index")
            
        except: 
            messages.info(request,"hata")
            return redirect("login")
        
