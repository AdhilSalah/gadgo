from unicodedata import name
from . import views
from django.urls import path

urlpatterns =[
    path('',views.checkout,name='checkout'),
    path('place_order',views.place_order,name='place_order'),
    path('payment_success/',views.payment_success,name='payment_success'),
    
    
]