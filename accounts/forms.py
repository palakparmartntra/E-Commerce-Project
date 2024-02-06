from django import forms
from .models import Address, User


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
    email = forms.RegexField(regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                             , error_messages={'invalid': 'Enter a valid email address.'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_no', 'email']
