from django.shortcuts import render



def signin(request):

    return render(request, 'login.html')



def signup(request):

    return render(request, 'signup.html')    
