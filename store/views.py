
from ast import keyword
import email
from itertools import count, product
from math import floor
from pyexpat.errors import messages
from queue import PriorityQueue
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from razorpay import Order

from carts.models import CartItem
from carts.views import _cart_id
from orders1.models import OrderProduct
from wishlists.models import WishlistItem
from wishlists.views import _wishlist_id, wishlist

from .models import Product, ProductImage, Review
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


def store(request, category_slug=None):
    categories = None
    store_products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)

        store_products = Product.objects.filter(
            category=categories, is_available=True)
        store_products_count = store_products.count()

    else:

        store_products = Product.objects.all().filter(
            is_available=True).order_by('-modified_date')
        store_products_count = store_products.count()

    
   
    for product in store_products:
        avg=0
        count=0
        avg_f=0
        rat_sum=0
        
        try:
            if Review.objects.filter(product=product).exists():
                
                review = Review.objects.filter(product=product)
                count=review.count()
                for m in review:
                    rating=m.rating
                    rat_sum += int(rating)
        except:
            pass    
        
       
        
        try:
            avg=rat_sum/count
        except ZeroDivisionError:
            pass    
    
        avg_f=floor(avg) 
        product.rating_dummy=avg_f
        product.save()  
    

    paginator = Paginator(store_products, 6)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'store_products': store_products,
        'store_producst_count': store_products_count,
        'page_obj': page_obj,

    }

    return render(request, 'store.html', context)


def product_details(request, category_slug, product_slug):
    count=0
    rat_sum=0
    avg_f=0
    avg=0

    try:

        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        side_images = ProductImage.objects.filter(product_id=single_product.id)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()

        in_wishlist = WishlistItem.objects.filter(
            wishlist__wishlist_id=_wishlist_id(request), product=single_product).exists()

        is_ordered = OrderProduct.objects.filter(
            user=request.user, product=single_product).exists()

    except Exception as e:
        raise e
    try:

        review = Review.objects.filter(product=single_product)

        count=review.count()
        for i in review:
            rating=i.rating
            rat_sum += int(rating)

        avg=rat_sum/count
        
        avg_f=floor(avg) 
        


        

    except ZeroDivisionError:
        pass

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'in_wishlist': in_wishlist,
        'side_images': side_images,
        'review': review,
        'is_ordered': is_ordered,
        'count':count,
        'avg_f':avg_f,
        'avg':avg
    }

    return render(request, 'product.html', context)


def search(request):

    if 'keyword' in request.GET:

        keyword = request.GET['keyword']

        if keyword:

            store_products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        else:

            store_products = Product.objects.all()
    paginator = Paginator(store_products, 6)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'store_products': store_products,
        'page_obj': page_obj,
    }

    return render(request, 'store.html', context)


def filter_product(request):

    if request.method == 'POST':

        min_price = request.POST['min_price']
        max_price = request.POST['max_price']
        cat_slug = 0

        try:
            url = request.META.get('HTTP_REFERER')

            category = Category.objects.all()
            for category in category:

                if '/category/'+category.slug in url:

                    cat_slug = category.slug

            categories = Category.objects.get(slug=cat_slug)

            store_products = Product.objects.all().filter(
                price__range=(min_price, max_price), category=categories)
        except Category.DoesNotExist:
            store_products = Product.objects.all().filter(
                price__range=(min_price, max_price))

    else:
        store_products = Product.objects.all()
    paginator = Paginator(store_products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'store_products': store_products,
        'page_obj': page_obj,
    }

    return render(request, 'store.html', context)


def review(request, product_id):
    user = request.user
    url = request.META.get('HTTP_REFERER')

    try:
        order = get_object_or_404(
            OrderProduct, user=user, product_id=product_id)
        

        product = Product.objects.get(id=product_id)

        if request.method == 'POST':

            content = request.POST['content']
            star = request.POST['rating']

            review = Review.objects.create(
                user=request.user,
                product=product,
                content=content,
                rating=star
            )
            review.save()

    except:
        pass

    return redirect(url)
