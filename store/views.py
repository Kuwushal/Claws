from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .static_data import get_featured_products, get_all_products, get_products_by_category, get_product_by_slug, get_all_categories, get_category_by_slug

def home(request):
    try:
        featured_products = get_featured_products()[:9]
        categories = get_all_categories()
        return render(request, 'store/home.html', {
            'featured_products': featured_products,
            'categories': categories
        })
    except Exception as e:
        messages.error(request, 'Error loading homepage')
        return render(request, 'store/home.html', {'featured_products': [], 'categories': []})

def product_list(request, category_slug=None):
    try:
        category = None
        categories = get_all_categories()
        
        if category_slug:
            category = get_category_by_slug(category_slug)
            if not category:
                messages.error(request, 'Category not found')
                return redirect('store:product_list')
            products = get_products_by_category(category_slug)
        else:
            products = get_all_products()
        
        return render(request, 'store/product_list.html', {
            'products': products,
            'category': category,
            'categories': categories
        })
    except Exception as e:
        messages.error(request, 'Error loading products')
        return render(request, 'store/product_list.html', {'products': [], 'categories': []})

def product_detail(request, slug):
    try:
        product = get_product_by_slug(slug)
        if not product:
            messages.error(request, 'Product not found')
            return redirect('store:product_list')
        return render(request, 'store/product_detail.html', {'product': product})
    except Exception as e:
        messages.error(request, 'Product not found')
        return redirect('store:product_list')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            size = request.POST.get('size')
            quantity = int(request.POST.get('quantity', 1))
            
            # Validation
            if not product_id or not size:
                return JsonResponse({'success': False, 'error': 'Missing required fields'})
            
            if quantity <= 0 or quantity > 99:
                return JsonResponse({'success': False, 'error': 'Invalid quantity'})
            
            product = get_object_or_404(Product, id=product_id)
            
            if quantity > product.stock:
                return JsonResponse({'success': False, 'error': 'Not enough stock available'})
            
            # Get or create cart
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart, created = Cart.objects.get_or_create(session_key=session_key)
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=size,
                defaults={'quantity': quantity}
            )
            
            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock:
                    return JsonResponse({'success': False, 'error': 'Not enough stock available'})
                cart_item.quantity = new_quantity
                cart_item.save()
            
            messages.success(request, f'{product.name} added to cart')
            return JsonResponse({'success': True})
            
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid quantity'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Error adding to cart'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def cart_view(request):
    try:
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
        
        return render(request, 'store/cart.html', {'cart': cart})
    except Exception as e:
        messages.error(request, 'Error loading cart')
        return render(request, 'store/cart.html', {'cart': None})

@login_required
def checkout(request):
    try:
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
        
        if not cart or not cart.items.exists():
            messages.error(request, 'Your cart is empty')
            return redirect('store:cart')
        
        return render(request, 'store/checkout.html', {'cart': cart})
    except Exception as e:
        messages.error(request, 'Error loading checkout')
        return redirect('store:cart')

@login_required
@require_http_methods(["POST"])
def process_paypal_payment(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('orderID')
        payment_id = data.get('paymentID')
        amount = data.get('amount')
        shipping_data = data.get('shipping_data', {})
        
        # Verify payment with PayPal
        if verify_paypal_payment(order_id, amount):
            # Create order in database
            cart = Cart.objects.filter(user=request.user).first()
            if not cart:
                return JsonResponse({'success': False, 'error': 'Cart not found'})
            
            order = Order.objects.create(
                user=request.user,
                total_amount=amount,
                payment_method='paypal',
                payment_id=payment_id,
                status='completed',
                shipping_address=f"{shipping_data.get('address', '')}, {shipping_data.get('city', '')}, {shipping_data.get('state', '')} {shipping_data.get('zip_code', '')}",
                email=shipping_data.get('email', ''),
                phone=shipping_data.get('phone', '')
            )
            
            # Create order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    price=item.product.price
                )
            
            # Clear cart
            cart.items.all().delete()
            
            return JsonResponse({'success': True, 'order_id': order.id})
        else:
            return JsonResponse({'success': False, 'error': 'Payment verification failed'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def verify_paypal_payment(order_id, expected_amount):
    """Verify PayPal payment with PayPal API"""
    try:
        # Get PayPal access token
        client_id = settings.PAYPAL_CLIENT_ID
        client_secret = settings.PAYPAL_CLIENT_SECRET
        
        # Use sandbox or live API based on settings
        base_url = 'https://api.sandbox.paypal.com' if settings.PAYPAL_MODE == 'sandbox' else 'https://api.paypal.com'
        
        auth_response = requests.post(
            f'{base_url}/v1/oauth2/token',
            headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
            data={'grant_type': 'client_credentials'},
            auth=(client_id, client_secret)
        )
        
        if auth_response.status_code != 200:
            return False
            
        access_token = auth_response.json()['access_token']
        
        # Verify order details
        order_response = requests.get(
            f'{base_url}/v2/checkout/orders/{order_id}',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        )
        
        if order_response.status_code == 200:
            order_data = order_response.json()
            payment_amount = float(order_data['purchase_units'][0]['amount']['value'])
            return abs(payment_amount - float(expected_amount)) < 0.01
            
        return False
    except Exception as e:
        print(f"PayPal verification error: {e}")
        return False

@login_required
def order_success(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})
@login_required
@require_http_methods(["POST"])
def process_card_payment(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        shipping_data = data.get('shipping_data', {})
        
        # Create order in database (simulate successful card payment)
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return JsonResponse({'success': False, 'error': 'Cart not found'})
        
        order = Order.objects.create(
            user=request.user,
            total_amount=amount,
            payment_method='card',
            payment_id='card_' + str(cart.id),
            status='completed',
            shipping_address=f"{shipping_data.get('address', '')}, {shipping_data.get('city', '')}, {shipping_data.get('state', '')} {shipping_data.get('zip_code', '')}",
            email=shipping_data.get('email', ''),
            phone=shipping_data.get('phone', '')
        )
        
        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                price=item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return JsonResponse({'success': True, 'order_id': order.id})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
@login_required
def profile(request):
    return render(request, 'store/profile.html', {'user': request.user})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'store/order_history.html', {'orders': orders})