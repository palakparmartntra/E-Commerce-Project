from django import forms
from .models import Product
from .models import Category
from .models import Brand
from .messages import BrandFormErrorMessages


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price', 'image', 'category', 'is_active']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'parent']

        # add css here in form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }


class AddBrandForm(forms.ModelForm):
    """" form to update brand details """

    name = forms.CharField(
        max_length=40,
        required=True,
        error_messages={'invalid': BrandFormErrorMessages.BRAND_NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Brand Name',
                'class': 'form-control'
            }
        )

    )

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Brand
        fields = [
            'name', 'image'
        ]


class UpdateBrandForm(forms.ModelForm):
    """" form to update brand details """

    name = forms.CharField(
        max_length=40,
        required=True,
        error_messages={'invalid': BrandFormErrorMessages.BRAND_NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Brand Name',
                'class': 'form-control'
            }
        )

    )

    class Meta:
        model = Brand
        fields = [
            'name', 'image'
        ]
