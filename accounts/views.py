
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from carts.models import Cart, CartItem
from carts.views import _cart_id
from category.models import Category
from orders1.models import Order, OrderProduct, Payment
from store.models import Product
from wishlists.models import Wishlist, WishlistItem
from wishlists.views import _wishlist_id
from .models import *
from django.contrib import messages
from accounts.models import Account
from django.contrib.auth.decorators import login_required









def signin(request):

    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email,password=password)
        
        if user is not None:

            try:    
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item:
                    cart_items= CartItem.objects.filter(cart=cart)
                    print(cart_items)


                    for cart_item in cart_items:

                    
                    
                        try :

                            
                            if CartItem.objects.filter(user=user).exists():

                                user_cart_items=CartItem.objects.filter(user=user)
                            else:    
                                user_cart_items= get_object_or_404(user=user)

                            print(user_cart_items)
                            

                                
                                

                            for user_cart_item in user_cart_items:
                                print('second_loop')

                                if str(cart_item) == str(user_cart_item):

                                    print(cart_item.quantity)
                                    print(user_cart_item.quantity)

                                    user_cart_item.quantity += cart_item.quantity


                                    user_cart_item.save()

                                else:

                                    cart_item.user=user
                                    cart_item.save()    





                        except :

                            print('in except')

                            cart_item.user=user
                            cart_item.save()
                    

                    # some = CartItem.objects.filter(user=user).exists()
                    # print(some)cart_items= CartItem.objects.filter(user=user)
                    # if some:

                    #     list=[]
                        

                    #     for item in cart_item:
                            

                        
                    #         cart_items= CartItem.objects.filter(user=user)
                    #         print(cart_items)
                    #         print(item)
                    #         # print(list)

                    #         for i in cart_items:
                    #             print(i)
                                
                            
                                

                    #             if str(item) == str(i):

                    #                 print('in_if')

                    #                 print(item.product.id)
                    #                 print(i.product.id)

                    #                 # pro = CartItem.objects.get(product__id = item.product.id)
                    #                 # print(pro)
                                    

                    #                 i.quantity += 1
                    #                 i.save()
                    #             else: 


                    #                 print('first_else')       


                                

                    #                 item.user=user
                    #                 item.save()

                    # else:      
                    #     print('second_else')  


                            

                    #     item.user=user
                    #     item.save()            
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
    top_pro = Product.objects.all().order_by('stock')




    context={
        'products':products,
        'category':category,
        'top_pro':top_pro,
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
            user = Account.objects.create_user(first_name=first_name, password=password1, email=email,last_name=last_name, phone_number=phone_number,is_active=True)

            user.save()
                
            messages.info(request, "sucess")
            return redirect(signin)


    return render(request,'signup.html') 


def user_details(request):

    if request.user.is_authenticated:

        address = ShippingAddress.objects.filter(user=request.user).exists() 

        user = Account.objects.get(id=request.user.id)

        context={
            'user':user,
            'address':address
        }



    return render(request,'user_details.html',context)


def edit_user(request):
    user=request.user

    
    if request.method=='POST' and 'edit_change' in request.POST:
            user=Account.objects.get(id=request.user.id)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone']
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Your Profile Is Edited')
            
    
    context={
        'user':user
    }

    return render(request,'edit_user.html',context) 

@login_required
def edit_password(request):
    current_user=request.user

    if request.method=='POST' and 'pass_change' in request.POST:
        user=Account.objects.get(id=current_user.id)
        pass1 = request.POST['pass1']
        pass2 =request.POST['pass2']
        print(pass1)

        if pass1=="" or pass2=="":
            messages.error(request,'Fields Cannot be Null')

        elif pass1==pass2:
            
            user.set_password(pass1)
            user.save()
            login(request,user)
            messages.success(request,'Password Changed')  
        else:
            messages.error(request,'Password not Same')      
    

    return redirect('edit_user') 

@login_required
def user_orders(request):
    user=request.user

    orders = Order.objects.filter(user=user)

    context={
        'orders':orders,
    }
    


    return render(request, 'user_orders.html',context)    


def user_order_details(request,order_id,total=0):

    order = Order.objects.get(id=order_id)
    payment = Payment.objects.get(id=order.payment.id)
    order_products = OrderProduct.objects.filter(payment_id=payment.id)
    
    for order_product in order_products:
            total += (order_product.product_price * order_product.quantity)
        

    context={
        'order':order,
        'payment':payment,
        'order_products':order_products,
        'total':total,
    }


    return render (request,'user_order_details.html',context)    

def user_default_address(request):

    address = ShippingAddress.objects.get(user=request.user)
    context={
        'address':address,
    }

    return render(request,'default_address.html',context)   


def edit_address(request):
    address = ShippingAddress.objects.get(user=request.user)

        

    if request.method=='POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address1 = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zipcode = request.POST['zipcode']

        
        address = ShippingAddress.objects.get(user=request.user)
        address.first_name = first_name
        address.last_name = last_name
        address.email = email
        address.phone = phone
        address.address = address1
        address.city = city
        address.state = state
        address.country = country
        address.zipcode = zipcode
        address.save()

        messages.success(request,'Address edited sucessfully')



        

    context={
        'address':address
    } 

    return render(request,'edit_address.html',context) 

def add_address(request):


    if request.method=='POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address1 = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zipcode = request.POST['zipcode']
        address=ShippingAddress.objects.create(
                user=request.user,
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone = phone,
                address = address1,
                city = city,
                state = state,
                country = country,
                zipcode = zipcode,
                
            )   
        address.save()
    return render(request,'edit_address.html') 


          







    

