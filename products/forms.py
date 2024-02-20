from django import forms
from .models import Category


class AddCategoryForm(forms.ModelForm):
"""This form contains all fields related to  add category"""
    class Meta:
        model = Category
        fields = ['name', 'image', 'parent']

        # add css here in form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }
