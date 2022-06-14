from django.urls import path
from store import views
from django.contrib import admin

from store.models import Product

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_details,name='product_details'),
    path('search',views.search,name='search'),
    path('filter_product/',views.filter_product,name='filter_product'),
    path('review/<int:product_id>/',views.review,name='review')

]
