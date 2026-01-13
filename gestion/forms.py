from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'file', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nom dutilisateur')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'cou', 'poignee', 'cheville', 'available', 'materiaux', 'numero']


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = [
            "name",
            "numero",
            "description",
            "category",
            "materiaux",
            "price",
            "image",
            "available",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom du produit",
            }),
            "numero": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Numéro interne",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Description du produit",
            }),
            "category": forms.Select(attrs={
                "class": "form-control",
            }),
            "materiaux": forms.Select(attrs={
                "class": "form-control",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "0.00",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "available": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }