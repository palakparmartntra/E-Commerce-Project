from django import forms
from .messages import BrandFormErrorMessages, SectionFormErrorMessages
from .models import Product, Category, Brand, Section, SectionItems, ContentType, Banner


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


class AddSectionForm(forms.ModelForm):
    """" form to update brand details """

    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),)

    name = forms.CharField(
        max_length=40,
        required=True,
        error_messages={'invalid': SectionFormErrorMessages.SECTION_NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Section Name',
                'class': 'form-control'
            }
        )
    )

    order = forms.IntegerField(
        required=True,
        error_messages={'invalid': SectionFormErrorMessages.ORDER},
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'class': 'form-control'
            }
        )
    )

    section_file = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    content_type = forms.ChoiceField(
        choices=CHOICES
    )

    class Meta:
        model = Section
        fields = [
            'name', 'order', 'section_file', 'content_type'
        ]


class AddSectionModelForm(forms.ModelForm):
    """" form to update brand details """

    APP_LABEL = 'products'
    MODELS = ('brand', 'category', 'product')
    model = ContentType.objects.values_list('id', flat=True).filter(app_label=APP_LABEL, model__in=MODELS)
    model_choices = zip(model, MODELS)

    content_type = forms.IntegerField(
        required=True,
        widget=forms.Select(
            choices=model_choices,
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = SectionItems
        fields = [
            'content_type'
        ]


class UpdateSectionForm(forms.ModelForm):
    """" form to update brand details """

    CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),)

    name = forms.CharField(
        disabled=True,
        max_length=100,
        required=True,
        error_messages={'invalid': SectionFormErrorMessages.SECTION_NAME},
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Section Name',
                'class': 'form-control'
            }
        )
    )
    order = forms.IntegerField(
        required=True,
        error_messages={'invalid': SectionFormErrorMessages.ORDER},
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Section
        fields = [
            'name', 'is_active', 'order', 'section_file'
        ]
