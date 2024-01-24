from django.shortcuts import render
from django.views.generic.edit import UpdateView
from .models import User, Address
from .forms import AddressForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.


class UpdateAddressView(UpdateView):
    """view for the update user address"""

    model = Address
    form_class = AddressForm
    template_name = 'update_address.html'
    success_url = reverse_lazy('index')


class UpdateUserProfile(UpdateView):
    """view for the update user profile"""

    model = User
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('index')
    context_object_name = 'data'


class Index(TemplateView):
    """view for the render index page """
    template_name = 'index.html'
