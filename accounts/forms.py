from django import forms
from .models import Address, User


class AddressForm(forms.ModelForm):
    """created form for update user address"""

    class Meta:
        model = Address
        fields = ['receiver_name', 'house_no', 'phone_no',
                  'street', 'landmark', 'city', 'state', 'zipcode']


class UserUpdateForm(forms.ModelForm):
    """created form for update user profile"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_no', 'email']
