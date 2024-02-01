from django import forms
from .models import Address, User
from allauth.account.forms import SignupForm
from django.core.validators import EmailValidator


class AddressForm(forms.ModelForm):
    """created form for update user address"""
    phone_no = forms.RegexField(min_length=10, max_length=10, regex=r'^\d+$',
                                error_messages={'invalid': 'Enter a valid integer.'})
    zipcode = forms.RegexField(max_length=6, min_length=6, regex=r'^\d+$',
                               error_messages={'invalid': 'Enter a valid integer.'})

    class Meta:
        model = Address
        fields = ['receiver_name', 'house_no', 'phone_no',
                  'street', 'landmark', 'city', 'state', 'zipcode']


class UserUpdateForm(forms.ModelForm):
    """created form for update user profile"""

    phone_no = forms.RegexField(min_length=10, max_length=10, regex=r'^\d+$',
                                error_messages={'invalid': 'Enter a valid integer.'})
    email = forms.RegexField(regex= '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                             ,
                             error_messages={'invalid': 'Enter a valid email address.'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_no', 'email']


class CustomSignupForm(SignupForm):
    """ created form for user signup """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        email_validator = EmailValidator(message="Enter a valid email address.")
        email_validator(email)
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # Your custom password validation logic here
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1
