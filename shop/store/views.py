from django.shortcuts import render
from . models import *
from django.http import JsonResponse
import json

# Create your views here.

# def store(request):
#     products = Product.objects.all().order_by('name')
#     return render(request, 'store/store.html',{'products':products})


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_quantity
    else:
        items = []
        order ={'get_cart_total':0,'get_cart_quantity':0}
        cartItems=order['get_cart_quantity']
    products =Product.objects.all().order_by('name')
    return render(request, 'store/store.html',{'products':products,'cartItems':cartItems})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_quantity()
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart',{}))
        except:
            cart = {}
            print('CART',cart)
        items = []
        order ={'get_cart_total':0,'get_cart_quantity':0}
        cartItems=order['get_cart_quantity']
       
        for i in cart:
            cartItems += cart[i]['quantity']
    return render(request, 'store/cart.html',{'items':items,'order':order,'cartItems':cartItems})


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_quantity
        
    else:
        items = []
        order ={'get_cart_total':0,'get_cart_quantity':0}
        cartItems=order['get_cart_quantity']
    return render(request, 'store/checkout.html',{'items':items,'order':order,'cartItems':cartItems})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ',action)
    print('ProductId : ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    # order,created =order.objects.get_or_create(customer=customer,complete=False)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    
    return JsonResponse('Item was added. ',safe=False)


