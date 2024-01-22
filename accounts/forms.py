from django import forms
from django.contrib.auth.models import User

class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
