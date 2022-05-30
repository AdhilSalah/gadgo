from django.urls import path
from wishlists import views


from store.models import Product

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
    path('remove_from_wishlist/<int:product_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    

]
