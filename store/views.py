
from django.shortcuts import get_object_or_404, render

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

    except Exception as e:
        raise e 


    context ={
        'single_product':single_product,
    }       




    return render(request,'product.html',context)    