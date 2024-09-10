from . models import *
import json

def CookieCart(request):
     try:
            cart = json.loads(request.COOKIES.get('cart','{}'))
     except:
            cart = {}
            print('CART',cart)

     items = []
     order ={'get_cart_total':0,'get_cart_quantity':0}
     cartItems=order['get_cart_quantity']
       
     for i in cart:  
            try:

                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_quantity'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                }

                items.append(item)
            except:
                pass
     return {'cartItems':cartItems,'order':order,'items':items}