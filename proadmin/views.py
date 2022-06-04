from multiprocessing import context
import unicodedata
from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from urllib3 import Retry
from category.models import Category
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.models import Account
from orders1.models import Order, OrderProduct, Payment


from store.models import Product

# Create your views here.
def super_home(request):
    if request.user.is_authenticated and request.user.is_superadmin:


        return render(request,'adminpro/index.html')
    return redirect('super_home_login')    



def products_view(request):
    if request.user.is_authenticated:


        products = Product.objects.all()

        context = {
            'products':products
        }


        return render(request,'adminpro/view_product.html',context)

    return redirect('super_home_login')        




def add_product(request):
    if request.user.is_authenticated and request.user.is_superadmin:



        if request.method == 'POST':
            product_name = request.POST['product_name']

            slug = slugify(product_name)
            stock = request.POST['stock']
            price = request.POST['price']
            category = Category.objects.get(id=request.POST['category'])
            description = request.POST['description']
            image = request.FILES.get('image')
            if product_name=="" or stock=="" or category=="" or image=="":
                messages.error(request,'Please fill all columns !')
            elif Product.objects.filter(product_name=product_name).exists():
                messages.error(request,'Item allready exists !')
            else:    


                product = Product.objects.create(product_name = product_name,slug=slug,stock=stock,price=price,category=category,description=description,image=image,is_available=True)

                product.save()




        return render(request,'adminpro/add_product.html')
    return redirect('super_home_login')    



def super_home_login(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect('super_home')

    if request.method=='POST':

        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email,password=password)
        print(user)
        if user is not None : 

            login(request,user)   

            return redirect('super_home')
        else:
            messages.error(request,'incorrect username or password')


    return render(request,'adminpro/super_signin.html')




def super_home_logout(request):

    if request.user.is_authenticated and request.user.is_superadmin:

        logout(request)

        return redirect('super_home_login')   



def super_home_orders(request):

    orders = Order.objects.filter(is_ordered=True)
    context={
        'orders':orders,
    }


    return render(request,'adminpro/admin_orders.html',context) 



def super_home_order_details(request,order_id,total=0):

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

    



    return render(request,'adminpro/admin_order_details.html',context)                        
