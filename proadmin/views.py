

from distutils.command.config import LANG_EXT
from math import floor
from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from category.models import Category
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.models import Account
from orders1.models import Order, OrderProduct, Payment


from store.models import Product, ProductImage

# Create your views here.
def super_home(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        total=0
        labels=[]
        data = []

        orders = Order.objects.all()

        for order in orders:

            total += order.order_total


            total = floor(total)


        products =  Product.objects.all()

        for product in products:
            labels.append(product.product_name[:10])
            data.append(product.stock)

        context={
            'products':products,
            'labels': labels,
            'data':data,
            'total':total,
        }


        return render(request,'adminpro/index.html',context)
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
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            
            if product_name=="" or stock=="" or category=="" or image=="":
                messages.error(request,'Please fill all columns !')
            elif Product.objects.filter(product_name=product_name).exists():
                messages.error(request,'Item allready exists !')
            else:    


                product = Product.objects.create(product_name = product_name,slug=slug,stock=stock,price=price,category=category,description=description,image=image,is_available=True)

                product.save()

                product = Product.objects.get(product_name=product_name)

                side_image1 = ProductImage.objects.create(product_id=product.id,image=image1)
                side_image1.save()
                side_image2 = ProductImage.objects.create(product_id=product.id,image=image2)
                side_image2.save()
                side_image3 = ProductImage.objects.create(product_id=product.id,image=image3)
                side_image3.save()
                messages.success(request,'Item added !')

            
        


               




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

    orders = Order.objects.order_by('-created_at').filter(is_ordered=True)
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





def edit_product(request,product_id):

    product = Product.objects.get(id=product_id)
    context={
        'product':product,

    }

    if request.method =='POST':
            product_name = request.POST['product_name']

            slug = slugify(product_name)
            stock = request.POST['stock']
            price = request.POST['price']
            description = request.POST['description']
            image = request.FILES.get('image')
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            
            if product_name=="" or stock=="" or price=="" or image=="":
                messages.error(request,'Please fill all columns !')
            
            else:    
                product.product_name = product_name
                product.slug =slug
                product.stock=stock
                product.price =price
                product.description = description
                product.image = image
                product.save()
                side_images = ProductImage.objects.filter(product_id=product_id)
                i=0
                images=(image1,image2,image3)
                for imageo in images:
                    
                    print('new image',imageo)
                    
                    image_new=side_images[i]
                    image_new.image=imageo
                    print('after assiging',image_new.image)
                    image_new.save()
                    i+=1
                    print('after saving',image_new.image)
                    
                    
                    
                
                messages.success(request,'Changed Saved !')
                
                

                

    return render(request,'adminpro/edit_product.html',context)  


def delete_product(request,product_id):

    product = Product.objects.get(id=product_id)
    product.delete()

    return redirect('products_view') 

def admin_user_details(request):

    users=Account.objects.order_by('-updated_date').filter(is_superadmin=False)
    context={
        'users':users,
    }

    return render(request,'adminpro/admin_user_details.html',context) 


def admin_user_activate(request,user_id):

    user=Account.objects.get(id=user_id)
    user.is_active=True
    user.save()


    return redirect('admin_user_details')

def admin_user_disable(request,user_id):

    user=Account.objects.get(id=user_id)
    user.is_active=False
    user.save()


    return redirect('admin_user_details')   

def payment_view(request):

    payment = Payment.objects.order_by('-created_at').all()

    context ={
        'payment':payment
    }


    return render(request,'adminpro/admin_payment.html',context)     


def edit_order(request,order_id):

    order = Order.objects.get(id=order_id)

    if request.method=='POST':

        status = request.POST['status']

        order.status=status
        order.save()

    return redirect('super_home_orders')    

