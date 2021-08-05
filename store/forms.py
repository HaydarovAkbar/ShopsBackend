from django import forms
from .models import Products,User
from django.contrib.auth.forms import UserCreationForm
class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category','product_name','price','image']

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
class Login(forms.Form):
    username = forms.CharField(label='Username: ',max_length=100)
    password = forms.CharField(label='Password: ',max_length=100)