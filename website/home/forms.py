# home/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, BlogPost, Comment # Added BlogPost, Comment

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

class ReservationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    number_of_guests = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 11)])
    selected_table = forms.CharField(widget=forms.HiddenInput(), required=True)
    special_requests = forms.CharField(widget=forms.Textarea, required=False)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'gender', 'address']

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

# --- NEW BLOG FORM ADDED BELOW ---

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content'] # User field will be set in view

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Get user if passed
        super().__init__(*args, **kwargs)

        # Apply basic styling class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        if user and user.is_authenticated:
            # Pre-populate fields if user is logged in
            self.fields['author_name'].initial = user.get_full_name() or user.username
            self.fields['author_email'].initial = user.email
            # Make name/email optional for logged-in users if you prefer them not to re-enter
            self.fields['author_name'].required = False
            self.fields['author_email'].required = False
        else:
            # For guests, make name required
            self.fields['author_name'].required = True