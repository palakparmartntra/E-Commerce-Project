from django import forms
from .models import Address,User

class AddressForm(forms.ModelForm):
        class Meta:
            model = Address
            fields = ['reciever_name','house_no','phone_no','street','landmark','city','state','zipcode']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
