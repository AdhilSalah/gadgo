
import random
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from carts.models import Cart, CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Product
from wishlists.models import Wishlist, WishlistItem
from wishlists.views import _wishlist_id
from .models import *
from django.contrib import messages
from accounts.models import Account








def signin(request):

    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email,password=password)
        
        if user is not None and not user.is_superadmin:

            try:    
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:

                        item.user=user
                        item.save()
            except:
                pass 

            try:    
                wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
                is_wishlist_item = WishlistItem.objects.filter(wishlist=wishlist).exists()

                if is_wishlist_item:
                    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist)
                    for item in wishlist_item:

                        item.user=user
                        item.save()
            except:
                pass                   

            login(request,user)
            return redirect(home)
            
            
            
        else:
            messages.error(request, "Incrorrect email or password")


            return redirect(signin)    

    return render(request, 'login.html')


def signout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(home)





def home(request):
    

    products=Product.objects.all().filter(is_available=True)
    category =Category.objects.all()

    context={
        'products':products,
        'category':category,
    }

    return render(request,'index.html',context) 




def signup(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method=='POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']    
        password2 = request.POST['password2']

        if Account.objects.filter(email=email).exists():
            messages.error(request, "email exists")

        elif Account.objects.filter(phone_number=phone_number).exists():
            messages.error(request,'phone mumber exist') 

        elif password1 !=password2:
            messages.error(request,'password not same')  

        else:
            user = Account.objects.create_user(first_name=first_name, password=password1, email=email,last_name=last_name, phone_number=phone_number)

            user.save()
                
            messages.info(request, "sucess")
            return redirect(signin)


    return render(request,'signup.html')     
