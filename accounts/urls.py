from django.urls import path
from accounts import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('user_details/', views.user_details, name='user_details'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('user_order_details/<int:order_id>/', views.user_order_details, name='user_order_details'),
    path('user_default_address/', views.user_default_address, name='user_default_address'),
    path('edit_address/', views.edit_address, name='edit_address'),
    path('add_address/', views.add_address, name='add_address'),
    # path('gologin/', views.gologin, name='gologin'),



]
