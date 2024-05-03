from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Product, Order, OrderItem, UserProfile
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import User

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

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:index')  # Ganti 'accounts:index' dengan URL halaman setelah login
        else:
            error = 'Invalid username or password'
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'order_history.html', {'orders': orders})

@receiver(user_logged_in, sender=User)
def update_last_login(sender, user, request, **kwargs):
    try:
        user.userprofile.save()
    except UserProfile.DoesNotExist:
        pass
