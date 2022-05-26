from django.urls import path
from store import views
from django.contrib import admin

from store.models import Product

urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:category_slug>/',views.store,name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_details,name='product_details'),

]
