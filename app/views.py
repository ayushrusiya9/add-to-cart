from django.shortcuts import render, redirect
from .models import Product

def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return render(request, 'shop/product_list.html', {'products': products, 'total_items': total_items})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart = request.session['cart']
    print(cart)

    product_id = str(product_id) 
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('product_list')

def remove_item(request, product_id):
    cart = request.session.get('cart', {})  # safe way to get cart
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            # quantity 0 ya negative ho → remove product from cart
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    print(cart)
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        subtotal = product.price * qty
        items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        print(items)
        total += subtotal
    total_items = sum(cart.values())
    return render(request, 'shop/cart.html', {'items': items, 'total': total, 'total_items': total_items})
