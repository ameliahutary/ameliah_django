from django.urls import path
from products.views import index

app_name = "products"

urlpatterns = [
    path("", index)
]