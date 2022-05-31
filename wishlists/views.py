
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

        if request.user.is_authenticated:
            wishlist_item = WishlistItem.objects.create(
            product=product,
            user = request.user,
            ) 

            wishlist_item.save
        else:    


            wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist = wishlist,
            ) 

            wishlist_item.save

    return redirect('wishlist')    





def wishlist(request,wishlist_items=None):


    try:
        if request.user.is_authenticated:
            wishlist_items=WishlistItem.objects.filter(user=request.user,is_active=True)
        else:    
            wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
            wishlist_items =WishlistItem.objects.filter(wishlist=wishlist,is_active = True)


    except Wishlist.DoesNotExist:
        pass

    context ={
        'wishlist_items':wishlist_items,
        
    }
    return render(request,'wishlist.html',context)




def remove_from_wishlist(request,product_id):

    wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    product = get_object_or_404(Product,id=product_id)

    if request.user.is_authenticated:
        Wishlist_item= WishlistItem.objects.get(product=product,user=request.user) 
    else:

        Wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist) 

    Wishlist_item.delete()

    return redirect('wishlist')