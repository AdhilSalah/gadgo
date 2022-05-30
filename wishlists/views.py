
from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from carts.views import _cart_id, cart

from store.models import Product
from .models import Wishlist,WishlistItem

# Create your views here.

def _wishlist_id(request):

    wishlist = request.session.session_key


    if not wishlist:
        wishlist = request.session.create()

        return wishlist


def add_wishlist(request,product_id):

    product = Product.objects.get(id=product_id)  
    try:

        wishlist =Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    except Wishlist.DoesNotExist:

        wishlist = Wishlist.objects.create(
            wishlist_id = _wishlist_id(request)
        )

        wishlist.save()


    try:
        wishlist_item = WishlistItem.objects.get(
            product=product,
            wishlist = wishlist,
        ) 

        return redirect('wishlist')

    except WishlistItem.DoesNotExist:

        wishlist_item = WishlistItem.objects.create(
            product=product,
            wishlist = wishlist,
        ) 

        wishlist_item.save

    return redirect('wishlist')    





def wishlist(request,wishlist_items=None):


    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
        wishlist_items =WishlistItem.objects.filter(wishlist=wishlist,is_active = True)


    except Wishlist.DoesNotExist:
        pass

    context ={
        'wishlist_items':wishlist_items,
        'cart_items':cart_items
    }
    return render(request,'wishlist.html',context)




def remove_from_wishlist(request,product_id):

    wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    product = get_object_or_404(Product,id=product_id)
    Wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist) 

    Wishlist_item.delete()

    return redirect('wishlist')