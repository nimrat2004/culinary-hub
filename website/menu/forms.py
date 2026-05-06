from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Review
from django import forms
from .models import Review , Order

class CustomRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review here...'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email_or_phone', 'payment_method', 'table_number']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select', 'id': 'paymentMethod'}),
        }
