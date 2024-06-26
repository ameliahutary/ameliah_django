import os
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_photos/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            width, height = img.size

            # Menentukan dimensi persegi yang diinginkan
            square_size = min(width, height)

            # Memotong gambar menjadi persegi
            left = (width - square_size) / 2
            top = (height - square_size) / 2
            right = (width + square_size) / 2
            bottom = (height + square_size) / 2

            img = img.crop((left, top, right, bottom))

            # Menyimpan gambar yang telah dipotong
            img.save(self.image.path)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Other fields as needed

    def __str__(self):
        return f"Cart for {self.user.username}"

@receiver(pre_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    # Hapus file gambar dari sistem file saat objek Photo dihapus
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating} Stars"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.CharField(max_length=100, blank=True)
    shipping_city = models.CharField(max_length=50, blank=True)
    shipping_country = models.CharField(max_length=50, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    # Tambahkan atribut lain yang sesuai dengan kebutuhan halaman HTML profile.html

    def __str__(self):
        return self.user.username

# Sinyal untuk membuat UserProfile saat pengguna baru mendaftar
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Sinyal untuk menyimpan UserProfile saat pengguna login untuk pertama kalinya
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Sinyal untuk membuat Cart saat pengguna baru mendaftar
@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
