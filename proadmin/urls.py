
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
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('admin_user_details',views.admin_user_details,name='admin_user_details'),
    path('admin_user_activate/<int:user_id>/',views.admin_user_activate,name='admin_user_activate'),
    path('admin_user_disable/<int:user_id>/',views.admin_user_disable,name='admin_user_disable'),
    path('payment_view/',views.payment_view,name='payment_view'),
    path('edit_order/<int:order_id>/',views.edit_order,name='edit_order'),


]