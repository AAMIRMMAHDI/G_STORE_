from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Cart, CartItem, Order
from products.models import Product, Packaging, Category

def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(
        session_key=session_key,
        defaults={'user': request.user if request.user.is_authenticated else None}
    )
    return cart

def cart(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    total_price = sum(item.quantity * item.packaging.price for item in cart_items if item.packaging) if cart_items else 0
    cart_count = cart.items.count()
    categories = Category.objects.all()
    
    shipping_cost = 500000
    discount_amount = 0
    final_amount = total_price + shipping_cost - discount_amount
    
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
        'categories': categories,
        'shipping_cost': shipping_cost,
        'discount_amount': discount_amount,
        'final_amount': final_amount,
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    packaging_id = request.POST.get('packaging_id')
    quantity = int(request.POST.get('quantity', 1))
    packaging = product.packagings.filter(id=packaging_id).first() if packaging_id else product.packagings.first()
    
    if not packaging:
        return JsonResponse({'error': 'بسته‌بندی انتخاب‌شده معتبر نیست.'}, status=400)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        packaging=packaging,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.items.count()})
    return redirect('products:product_detail', pk=product_id)

def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        total_price = sum(item.quantity * item.packaging.price for item in cart.items.all() if item.packaging)
        shipping_cost = 50000
        discount_amount = 0
        final_amount = total_price + shipping_cost - discount_amount
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.items.count(),
            'total_price': total_price,
            'shipping_cost': shipping_cost,
            'discount_amount': discount_amount,
            'final_amount': final_amount,
        })
    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)

def remove_from_cart(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    total_price = sum(item.quantity * item.packaging.price for item in cart.items.all() if item.packaging)
    shipping_cost = 50000
    discount_amount = 0
    final_amount = total_price + shipping_cost - discount_amount
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.items.count(),
            'total_price': total_price,
            'shipping_cost': shipping_cost,
            'discount_amount': discount_amount,
            'final_amount': final_amount,
        })
    return redirect('cart:cart')

def checkout(request):
    if request.method == 'POST':
        cart = get_cart(request)
        if not cart.items.exists():
            return render(request, 'cart/cart.html', {
                'error': 'سبد خرید شما خالی است.',
                'cart': cart,
                'cart_items': [],
                'total_price': 0,
                'cart_count': 0,
                'categories': Category.objects.all(),
                'shipping_cost': 0,
                'discount_amount': 0,
                'final_amount': 0,
            })
        
        order, created = Order.objects.get_or_create(
            cart=cart,
            defaults={
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
                'province': request.POST.get('province'),
                'city': request.POST.get('city'),
                'address': request.POST.get('address'),
                'notes': request.POST.get('notes', ''),
                'total_amount': cart.total_price(),
                'status': 'confirmed',
                'confirmed_at': timezone.now(),
            }
        )
        if not created:
            order.first_name = request.POST.get('first_name')
            order.last_name = request.POST.get('last_name')
            order.phone = request.POST.get('phone')
            order.email = request.POST.get('email')
            order.province = request.POST.get('province')
            order.city = request.POST.get('city')
            order.address = request.POST.get('address')
            order.notes = request.POST.get('notes', '')
            order.total_amount = cart.total_price()
            order.status = 'confirmed'
            order.confirmed_at = timezone.now()
            order.save()
        
        return redirect('cart:order_detail', order_id=order.order_id)
    
    return redirect('cart:cart')

def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.is_viewed = True
    order.save()
    
    cart_items = order.cart.items.all()
    total_price = order.total_amount
    shipping_cost = 50000
    discount_amount = 0
    final_amount = total_price + shipping_cost - discount_amount
    
    return render(request, 'cart/order_detail.html', {
        'order': order,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'discount_amount': discount_amount,
        'final_amount': final_amount,
    })