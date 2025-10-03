from django.shortcuts import render, redirect
from .models import Product,ProductCart
import razorpay
from django.views.decorators.csrf import csrf_exempt


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
    cart = request.session.get('cart', {})  
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


def payment(request):
    global payment
    if request.method=="POST":
        # amount in paisa
        amount = float(request.POST.get('amount')) * 100
        
        client = razorpay.Client(auth =("rzp_test_RNMrrOvCpxy6Gi" , "0ZyX31W7ienxCwVA8KbgEVgd"))
        # create order
        
        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        product = ProductCart.objects.create( amount =amount , order_id = payment['id'])
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
        return render(request, 'shop/cart.html', {'items': items, 'total': total, 'total_items': total_items,'payment':payment})

@csrf_exempt
def payment_status(request):
    if request.method == "POST": 
        response = request.POST   # frontend se form-data aa raha hai (razorpay ka response)
        print(response.get('razorpay_payment_id'))
        razorpay_data = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature')
        }

        # Razorpay client instance
        client = razorpay.Client(auth=("rzp_test_RNMrrOvCpxy6Gi", "0ZyX31W7ienxCwVA8KbgEVgd"))
    try:
        print("Verifying signature with:", razorpay_data)
        # Signature verify karna
        client.utility.verify_payment_signature(razorpay_data)  # ye sirf validate karta hai

        # Agar signature sahi hai, ye code execute hoga
        product = ProductCart.objects.get(order_id=razorpay_data['razorpay_order_id'])
        product.razorpay_payment_id = razorpay_data['razorpay_payment_id']
        product.paid = True
        product.save()
        
        print("Payment saved successfully:", product.razorpay_payment_id)
        return render(request, 'shop/success.html', {'status': True})

    except razorpay.errors.SignatureVerificationError as e:
        print("Signature verification failed:", e)
    except ProductCart.DoesNotExist:
        print("Order not found in ProductCart")
    except Exception as e:
        print("Unknown error:", repr(e))

    return render(request, 'shop/success.html', {'status': False})
