from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, UserProfile

def index(request):
    return render(request, 'home.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def cart(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    order, created = Order.objects.get_or_create(user=request.user, status='Pending')
    items = OrderItem.objects.filter(order=order)

    # Ambil produk yang terkait dengan setiap OrderItem
    products = [item.product for item in items]

    return render(request, 'cart.html', {'items': items, 'products': products, 'profile': user_profile})


@login_required
def checkout(request):
    # Implement checkout logic here
    return render(request, 'checkout.html')

def user_login(request):
    # Implement user login logic here
    return render(request, 'login.html')

def user_register(request):
    # Implement user registration logic here
    return render(request, 'register.html')

@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'order_history.html', {'orders': orders})
