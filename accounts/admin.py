from django.contrib import admin
from .models import Product, Order, OrderItem, UserProfile, ProductReview, Photo

class PhotoInline(admin.TabularInline):  
    model = Photo
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [PhotoInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status')
    search_fields = ('user__username',)
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'date_added')
    search_fields = ('order__id', 'product__name',)
    list_filter = ('date_added',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'country')
    search_fields = ('user__username', 'address')
    list_filter = ('country',)

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username',)
    list_filter = ('product__category',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

