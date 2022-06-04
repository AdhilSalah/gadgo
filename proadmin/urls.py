
from proadmin import views
from django.urls import path

urlpatterns =[
    path('',views.super_home,name='super_home'),
    path('products_view/',views.products_view,name='products_view'),
    path('add_product/',views.add_product,name='add_product'),
    path('super_home_logout/',views.super_home_logout,name='super_home_logout'),
    path('super_home_login/',views.super_home_login,name='super_home_login'),
    path('super_home_orders/',views.super_home_orders,name='super_home_orders'),
    path('super_home_order_details/<int:order_id>/',views.super_home_order_details,name='super_home_order_details'),
    

]