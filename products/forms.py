from django import forms
from .models import Category


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'parent']

        # add css here in form
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),

        }
