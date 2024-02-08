from django import forms
from .models import Address, User
from .constant import FormRegex
from .messages import UserFormErrorMessages


class UserUpdateForm(forms.ModelForm):
    """created form for update user profile"""

    first_name = forms.RegexField(
        max_length=25,
        regex=FormRegex.NAME,
        error_messages={'invalid': UserFormErrorMessages.NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }
        )
    )

    last_name = forms.RegexField(
        max_length=25,
        regex=FormRegex.NAME,
        error_messages={'invalid': UserFormErrorMessages.NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'
            }
        )
    )
    phone_no = forms.RegexField(
        min_length=10,
        max_length=10,
        regex=FormRegex.PHONE_NO,
        error_messages={'invalid': UserFormErrorMessages.PHONE_NO},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Contact',
                'class': 'form-control'
            }
        )
    )
    email = forms.RegexField(
        regex=FormRegex.EMAIL,
        error_messages={'invalid': UserFormErrorMessages.EMAIL},
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email address',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_no', 'email'
        ]


class AddAddressForm(forms.ModelForm):
    """created form for update user profile"""

    receiver_name = forms.RegexField(
        max_length=25,
        regex=FormRegex.NAME,
        error_messages={'invalid': UserFormErrorMessages.NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Receiver Name',
                'class': 'form-control'
            }
        )
    )

    house_no = forms.CharField(
        required=True,
        max_length=8,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'House no.',
                'class': 'form-control'
            }
        )
    )

    phone_no = forms.RegexField(
        required=True,
        min_length=10, max_length=10, regex=FormRegex.PHONE_NO,
        error_messages={'invalid': UserFormErrorMessages.PHONE_NO},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Contact',
                'class': 'form-control'
            }
        )
    )
    street = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Street',
                'class': 'form-control'
            }
        )
    )

    landmark = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Landmark',
                'class': 'form-control'
            }
        )
    )

    city = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City',
                'class': 'form-control'}
        )
    )

    state = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'State',
                'class': 'form-control'
            }
        )
    )

    zipcode = forms.CharField(
        required=True,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Zipcode',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Address
        fields = [
            'receiver_name', 'house_no', 'phone_no', 'street',
            'landmark', 'city', 'state', 'zipcode'
        ]
