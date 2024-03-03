from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .cart import Cart
from apps.product.models import Product


def add_to_cart(request, product_slug):
    cart = Cart(request)
    cart.add(product_slug)

    return render(request, 'cart/partials/menu_cart.html',{cart:'cart'})

def cart(request):
    session_data = request.session
    
    # Print session data
    for key, value in session_data.items():
        print(f"{key}: {value}")
    return render(request, 'cart/cart.html')

def success(request):
    return render(request, 'cart/success.html')

def update_cart(request, product_id, action):
    cart = Cart(request)

    if action == 'increment':
        print('-------->','Increment')
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)
    
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    
    if quantity:
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.get_thumbnail_url,
                'get_thumbnail_url': product.get_thumbnail_url,
                'price': product.price,
            },
            'total_price': (quantity * product.price) / 100,
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response

@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE 
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')

