from django import forms
from .models import Product, Category, Brand, Banner
from .messages import BrandFormErrorMessages


class AddProductForm(forms.ModelForm):
    """ this forms contains all fields related to add products"""

    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price', 'image', 'category', 'brand']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class UpdateProductForm(forms.ModelForm):
    """this form contains all fields related to update products"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price', 'image', 'category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class AddCategoryForm(forms.ModelForm):
    """This form contains all fields related to  add category"""

    class Meta:
        model = Category
        fields = ['name', 'image', 'parent']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
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


class AddBannerForm(forms.ModelForm):
    """ This form is useful to add banner """

    class Meta:
        model = Banner
        fields = ['banner_name', 'banner_image']

        widgets = {
            'banner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UpdateBannerForm(forms.ModelForm):
    """ This form is useful to update banner"""

    class Meta:
        model = Banner
        fields = ['banner_name', 'banner_image', 'is_active']

        widgets = {
            'banner_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
