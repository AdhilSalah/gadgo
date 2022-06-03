import datetime
from time import strftime
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render,redirect

from carts.models import CartItem
from orders1.models import Order
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def checkout(request,total=0,quantity=0):
    if request.user.is_authenticated:

        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity

        context={
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
        }    

    return render(request,'checkout.html',context)


def place_order(request,quantity=0):
    total=0
    tax=0
    grand_total=0
    

    if request.user.is_authenticated:

        current_user = request.user

        
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax = (2*total)/100
        grand_total =total+tax  

        if request.method=='POST':

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            address = request.POST['address']
            country = request.POST['country']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zip_code']
            order_note = request.POST['order_note']
            order = Order.objects.create(
                user= current_user,
                first_name=first_name,
                last_name=last_name,
                phone=phone_number,
                email=email,
                address_line_1=address,
                country=country,
                city=city,
                state=state,
                zipcode=zipcode,
                order_note=order_note,
                order_total=grand_total,
                tax = tax,
                
            )
            order.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d= datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            o_id = order.id
            order_number = current_date+str(o_id)
            order.order_number = order_number
            order.save()

            order = Order.objects.get(user=current_user,is_ordered = False,order_number=order_number)
            
            client = razorpay.Client(auth=("rzp_test_OFFUs9LlryRh7O", "WpC74jjkJpVzGFSEjyoPKycq"))
            sum=int(grand_total)

            data = ({ "amount": sum, "currency": "INR", "payment_capture":"1" })
            response = client.order.create(data=data)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':grand_total,
                'tax':tax,
                'response':response,
                'sum':sum,
            }


            

            return render(request,'payment.html',context)

        return redirect('cart')    
            


    return redirect('cart') 


@csrf_exempt
def payment_success(request):
    if request.method =="POST":
        print(request.POST)
        return HttpResponse("Done payment hurrey!")



     
