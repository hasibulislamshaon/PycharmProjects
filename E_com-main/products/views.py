from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
import json
import datetime
from . utils import cookieCart,cartData,guestOrder

# Create your views here.
def store(request):

    Data = cartData(request)
    cartItems = Data['cartItems']
    products = Product.objects.all()
    context={'products':products, 'cartItems':cartItems}
    return render(request,"store.html",context)

def cart(request):
    
    Data = cartData(request)
    cartItems = Data['cartItems']
    order=Data['order']
    items = Data['items']



    context={'items':items,'order':order, 'cartItems':cartItems}
    return render(request,"cart.html",context)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def cheakout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order=Data['order']
    items = Data['items']
       

    context={'items':items,'order':order, 'cartItems':cartItems}
    return render(request,"cheakout.html",context)

def updateItem(request):
    data = json.loads(request.body)
    productId= data['productId']
    action= data['action']

    print('Action:',action)
    print('productId:',productId)

    customer=request.user.customer
    product = Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <+ 0:
        orderItem.delete()
    return JsonResponse('Item was Added', safe=False)


def processOrder(request):
    transection_id= datetime.datetime.now().timestamp()
    data = json.loads(request.body)


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer =customer,complete=False)
        
    else:
       customer,order = guestOrder(request,data)
    total = float(data['form']['total'])
    order.transection_id=transection_id

    if total == order.get_cart_total:
        order.complete =True
    order.save()
    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    
    return JsonResponse('Payment Complete', safe=False)

def view(request, productId):
    product = get_object_or_404(Product, name=productId)
    context={'product':product}
    return render(request,"view.html",context)


