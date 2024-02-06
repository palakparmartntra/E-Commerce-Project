from django import forms
from .models import Address, User
from .constant import FormRegex


class AddressForm(forms.ModelForm):
    """created form for update user address"""
    phone_no = forms.RegexField(
        min_length=10,
        max_length=10,
        regex=FormRegex.EMAIL_REGEX,
        error_messages={'invalid': 'Enter a valid integer.'})
    zipcode = forms.RegexField(
        max_length=6,
        min_length=6,
        regex=FormRegex.ZIPCODE_REGEX,
        error_messages={'invalid': 'Enter a valid integer.'})

    class Meta:
        model = Address
        fields = [
            'receiver_name', 'house_no', 'phone_no',
            'street', 'landmark', 'city', 'state', 'zipcode'
        ]


class UserUpdateForm(forms.ModelForm):
    """created form for update user profile"""

    first_name = forms.RegexField(
        max_length=30,
        regex=FormRegex.NAME,
        error_messages={'invalid': 'Enter a valid integer.'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }
        )
    )

    last_name = forms.RegexField(
        max_length=30,
        regex=FormRegex.NAME,
        error_messages={'invalid': 'Enter a valid integer.'},
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
        error_messages={'invalid': 'Enter a valid integer.'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Contact',
                'class': 'form-control'
            }
        )
    )
    email = forms.RegexField(
        regex=FormRegex.EMAIL_REGEX,
        error_messages={'invalid': 'Enter a valid email address'},
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

    receiver_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Receiver Name',
                'class': 'form-control'
            }
        )
    )

    house_no = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'House no.',
                'class': 'form-control'
            }
        )
    )

    phone_no = forms.RegexField(
        min_length=10, max_length=10, regex=FormRegex.PHONE_NO,
        error_messages={'invalid': 'Enter a valid Phone number.'},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Contact',
                'class': 'form-control'
            }
        )
    )
    street = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Street',
                'class': 'form-control'
            }
        )
    )

    landmark = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Landmark',
                'class': 'form-control'
            }
        )
    )

    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City',
                'class': 'form-control'}
        )
    )

    state = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'State',
                'class': 'form-control'
            }
        )
    )

    zipcode = forms.CharField(
        max_length=30,
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
