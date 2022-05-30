import unicodedata
from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from category.models import Category
from django.utils.text import slugify
from django.contrib import messages


from store.models import Product

# Create your views here.
def super_home(request):

    return render(request,'adminpro/index.html')



def products_view(request):


    products = Product.objects.all()

    context = {
        'products':products
    }


    return render(request,'adminpro/view_product.html',context)    




def add_product(request):


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