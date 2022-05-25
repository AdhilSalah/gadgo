
import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from elctro.views import home
from .mixins import *
from .models import *
from django.contrib import messages








def signin(request):

    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email,password=password)
        
        if user is not None:
            user =Account.objects.get(email=email)

            user.otp = random.randint(1000,9999)
            user.save()
            request.session['id']= user.id
            messsage_handler=MessageHandler(user.phone_number,user.otp).send_otp_on_phone()
            return redirect('otpverify')
            
        else:
            messages.error(request, "Incrorrect email or password")


            return redirect(signin)    

    return render(request, 'login.html')


def signout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(home)



def otpverify(request):

    if request.method=='POST':
        id = request.session['id']
        otp =request.POST['otp']
        user =Account.objects.get(id=id)
        if user.otp == otp:
            login(request,user)
            return redirect(home)
        else:
            return redirect(signin)    





    return render(request,'otp.html')   


def home(request):

    return render(request,'index.html') 




def signup(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method=='POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']    
        password2 = request.POST['password2']

        if Account.objects.filter(email=email).exists():
            messages.error(request, "email exists")

        elif Account.objects.filter(phone_number=phone_number).exists():
            messages.error(request,'phone mumber exist') 

        elif password1 !=password2:
            messages.error(request,'password not same')  

        else:
            user = Account.objects.create_user(first_name=first_name, password=password1, email=email,last_name=last_name, phone_number=phone_number)

            user.save()
                
            messages.info(request, "sucess")
            return redirect(signin)


    return render(request,'signup.html')     
