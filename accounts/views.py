from django.shortcuts import render
# testing
from django.views.generic.edit import UpdateView
from .models import User, Address
from .forms import AddressForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.views.generic.detail import DetailView
from .models import User


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


class Index(TemplateView):
    """view for the render index page """
    template_name = 'index.html'


class ViewProfile(DetailView):
    """ To view user details """
    model = User
    template_name = 'profile/view_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['addresses'] = user.address.all()
        return context
