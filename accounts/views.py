from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from .models import Address
from .forms import AddressForm, UserUpdateForm, AddAddressForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import modelformset_factory
from django.contrib import messages


class HomePageView(TemplateView):
    """ view for rendering index page """

    template_name = 'index.html'


@method_decorator(login_required, name='dispatch')
class AddAddress(CreateView):
    """ To create a new address """

    model = Address
    template_name = 'profile/add_address.html'
    form_class = AddAddressForm

    def form_valid(self, form):
        if Address.objects.filter(user=self.request.user).count() < 3:
            form.instance.is_primary = True
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


def address(request):
    """" To show and update all the addresses of user the current user """

    AddressFormSet = modelformset_factory(Address, form=AddAddressForm, extra=0)
    address_form = AddressFormSet(request.POST)
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        if address_form.is_valid():
            address_form.save()
            messages.success(request, "Address updated successfully")
            return redirect(to="profile")
    else:
        address_form = AddressFormSet(queryset=addresses)
    profile_form = UserUpdateForm(instance=User.objects.get(username=request.user))
    return render(request, 'profile/profile.html', {
        "profile_form": profile_form,
        "address_form": address_form,
        "addresses": addresses
    })


@login_required
def profile(request):
    """" To show and update user details of the current user """

    addresses = Address.objects.filter(user=request.user)
    if request.method == "POST":
        profile_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully")

    else:
        profile_form = UserUpdateForm(instance=User.objects.get(username=request.user))
    AddressFormSet = modelformset_factory(Address, form=AddAddressForm, extra=0)
    address_form = AddressFormSet(queryset=Address.objects.filter(user=request.user))
    return render(request, 'profile/profile.html', {
        "profile_form": profile_form,
        "address_form": address_form,
        "addresses": addresses
    })
