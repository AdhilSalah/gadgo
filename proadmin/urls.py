
from proadmin import views
from django.urls import path

urlpatterns =[
    path('',views.super_home,name='super_home'),
    path('products_view/',views.products_view,name='products_view'),
    path('add_product/',views.add_product,name='add_product'),

]