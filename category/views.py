from django.shortcuts import render

# Create your views here.

from itertools import product
from django.shortcuts import get_object_or_404, render

from carts.models import CartItem
from carts.views import _cart_id
from wishlists.models import WishlistItem
from wishlists.views import _wishlist_id, wishlist

from .models import Product
from category.models import Category

# Create your views here.


def store(request,category_slug=None):
    categories = None
    store_products = None

    if category_slug!=None:
        categories = get_object_or_404(Category,slug = category_slug)

        store_products   =Product.objects.filter(category=categories,is_available=True)
        store_products_count = store_products.count()
        
    else:
        
        store_products = Product.objects.all().filter(is_available=True)
        store_products_count = store_products.count()
        

    context={

        'store_products':store_products,
        'store_producst_count':store_products_count,
    }

    return render(request,'store.html',context)




def product_details(request,category_slug,product_slug):

    try:

        single_product =Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart =CartItem.objects.filter(cart__cart_id = _cart_id(request),product=single_product).exists()

        in_wishlist = WishlistItem.objects.filter(wishlist__wishlist_id = _wishlist_id(request),product=single_product).exists()

    except Exception as e:
        raise e 


    context ={
        'single_product':single_product,
        'in_cart':in_cart,
        'in_wishlist':in_wishlist,
    }       




    return render(request,'product.html',context)   