from django.shortcuts import render

from django.views.generic.edit import UpdateView, CreateView
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

    def get_success_url(self):
        user_id = self.object.user.pk
        return reverse_lazy('view_profile', kwargs={'pk': user_id})


class UpdateUserProfile(UpdateView):
    """view for the update user profile"""

    model = User
    form_class = UserUpdateForm
    template_name = 'update_profile.html'

    def get_success_url(self):
        user_id = self.object.pk
        return reverse_lazy('view_profile', kwargs={'pk': user_id})


class Index(TemplateView):
    """view for the render index page """
    template_name = 'index.html'


class ViewProfile(DetailView):
    """ To view user details """
    model = User
    template_name = 'profile/view_profile.html'
    context_object_name = 'user'

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['addresses'] = user.address.all()
        return context


class HomePageView(TemplateView):
    """ view for rendering index page"""

    template_name = 'index.html'


class AddAddress(CreateView):
    model = Address
    fields = ['receiver_name', 'house_no', 'phone_no', 'street',
              'landmark', 'city', 'state', 'zipcode']
    template_name = 'profile/add_address.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.request.user.pk})
