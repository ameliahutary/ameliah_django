from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('products/<int:product_id>/submit-review/', views.submit_product_review, name='submit_product_review'),
    path('products/<int:product_id>/related-products/', views.related_products, name='related_products'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('order_history/', views.order_history, name='order_history'),
] 