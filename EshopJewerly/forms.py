from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Category, Manufacturer, Product

from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'name', 'surname', 'address']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'address']


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all())
    gender = forms.ChoiceField(choices=Product.GENDER_CHOICES)

    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'category', 'manufacturer', 'gender', 'image']

class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)