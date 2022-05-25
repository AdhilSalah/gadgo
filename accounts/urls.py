from django.urls import path
from accounts import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('otpverify/', views.otpverify, name='otpverify'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),

]
