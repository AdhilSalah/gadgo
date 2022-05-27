from unicodedata import name
from carts import views
from django.urls import path

urlpatterns =[
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name="remove_cart"),
    path('remove_item_fully/<int:product_id>/',views.remove_item_fully,name='remove_item_fully'),
]