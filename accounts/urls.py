from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('order_history/', views.order_history, name='order_history'),
] 