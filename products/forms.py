from django import forms
from .models import Product
from .models import Category


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price', 'image', 'category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'})
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'parent']

        # add css here in form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }
