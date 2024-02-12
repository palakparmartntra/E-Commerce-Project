from django import forms
from .models import Brand
from .messages import BrandFormErrorMessages


class BrandForm(forms.ModelForm):
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
        fields = "__all__"
