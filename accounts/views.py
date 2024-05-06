from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Product, ProductReview, Order, OrderItem, UserProfile
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from .forms import ProfilePictureForm
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404


def index(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'home.html', {'user_profile': user_profile})

def about(request):
    return render(request, 'about.html')


def products(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'user_profile': user_profile})

def product_detail(request, product_id):  
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    product = Product.objects.get(id=product_id)
    photos = product.photos.all()
    reviews = ProductReview.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'user_profile': user_profile})



def add_to_wishlist(request, product_id):
    # Implementasi logika untuk menambahkan produk ke daftar keinginan
    pass

def submit_product_review(request, product_id):
    # Implementasi logika untuk menyimpan ulasan produk baru
    pass

def related_products(request, product_id):
    # Implementasi logika untuk menampilkan produk terkait
    pass


def profile(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})


@login_required
def cart(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    order, created = Order.objects.get_or_create(user=request.user, status='Pending')
    items = OrderItem.objects.filter(order=order)

    # Ambil produk yang terkait dengan setiap OrderItem
    products = [item.product for item in items]

    # Hitung total harga
    total_price = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart.html', {'items': items, 'products': products, 'user_profile': user_profile, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status='Pending')
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Jika order item sudah ada dalam keranjang, tambahkan satu ke jumlahnya
    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect('accounts:cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.delete()
    return redirect('accounts:cart')


@login_required
def checkout(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    # Implement checkout logic here
    return render(request, 'checkout.html', {'checkout': checkout, 'user_profile': user_profile})

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:index')  
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

@login_required
def some_view(request):
    return render(request, 'some_template.html', {'user': request.user})


def logout_view(request):
    # Lakukan logout pengguna
    logout(request)
    # Redirect pengguna ke halaman lain, misalnya halaman beranda
    return redirect('accounts:index')