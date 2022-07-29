from django import forms
from .models import Order, Product, Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'username', 'email', 'company', 'shipping_address', 'city', 'province',
                  'interested_in', 'profile_picture',
                  'password1', 'password2',)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client',
                  'product',
                  'num_units']
        widgets = {
            'client': forms.RadioSelect,
        }

        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }


class InterestForm(forms.Form):
    Choices = [('1', 'Yes'), ('0', 'No')]
    interested = forms.ChoiceField(choices=Choices, widget=forms.RadioSelect)
    quantity = forms.DecimalField(initial=1)
    comments = forms.CharField(widget=forms.Textarea(), label="Additional Info")
