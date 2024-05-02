from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'city', 'country']

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(max_length=100)
    shipping_city = forms.CharField(max_length=50)
    shipping_country = forms.CharField(max_length=50)
    payment_method = forms.ChoiceField(choices=[('COD', 'Cash on Delivery'), ('Card', 'Credit/Debit Card')])
