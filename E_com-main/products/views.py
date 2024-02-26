from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
import datetime
from . utils import cookieCart,cartData,guestOrder
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm
from django.contrib.auth  import authenticate,login,logout 
from django.contrib import messages
import stripe
# Create your views here.

stripe.api_key = 'sk_test_51NEzSiFDYydnnbweNQ7Zxtt0IScFIdxJc4nUyrU5cUgkI4XwJIvpc7BFxrEgl8QafrfzNnXcuhPF3UgFErFfjabo004X2vZ70O'


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

def view(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,"view.html",context)
""""
def registerPage(request):
    form=CreateUserForm()


    if request.method == 'POST':
       form= CreateUserForm(request.POST)
       if form.is_valid():
           form.save()
           user = form.cleaned_data.get('username')
           messages.success(request, 'User is created as ' + user)
           return redirect('login')
 
    context ={'form':form}
    return render(request,'register.html',context)
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('store')
        else: 
            messages.info(request,'Username or password is incorrect')
            return redirect('login')
    context ={}
    return render ( request,'login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('store')"""

