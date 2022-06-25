
from django.shortcuts import get_object_or_404, redirect, render
from orders1.models import Order

from store.models import Product
from .models import Cart,CartItem

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)

    


    try:
        cart =Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:

        cart =Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()


    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user)
        else:
            cart_item =CartItem.objects.get(product=product,cart=cart)

        cart_item.quantity += 1

        cart_item.save()

    except CartItem.DoesNotExist:

        if request.user.is_authenticated:
            cart_item =CartItem.objects.create(
            product=product,
            quantity =1,
            user =request.user,
             ) 
            cart_item.save()

        else:    
            cart_item =CartItem.objects.create(
            product=product,
                quantity =1,
                cart =cart,
            ) 
            cart_item.save()
        


    return redirect('cart')             


def cart(request,total=0,quantity=0,tax=0,grand_total=0,cart_items=None):

    Order.objects.filter(is_ordered=False).delete()

    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('-created_date')

        else:    
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('-created_date')
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax    
            
    except Cart.DoesNotExist:

        pass      



    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    } 

    return render(request,'cart.html',context)





def remove_cart(request,product_id):
    
    product = get_object_or_404(Product,id=product_id)

    if request.user.is_authenticated:
        cart_item= CartItem.objects.get(product=product,user=request.user)

    else:   
        cart =Cart.objects.get(cart_id=_cart_id(request)) 
        cart_item= CartItem.objects.get(product=product,cart=cart)

    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()

    else:
        cart_item.delete()    


    return redirect('cart')  



def remove_item_fully(request,product_id):
    
    product = get_object_or_404(Product,id=product_id)

    if request.user.is_authenticated:
        cart_item =CartItem.objects.filter(product=product,user=request.user)

    else:    
        cart = Cart.objects.get(cart_id=_cart_id(request))  
        cart_item =CartItem.objects.filter(product=product,cart=cart)



    cart_item.delete()

    return redirect('cart')  


   