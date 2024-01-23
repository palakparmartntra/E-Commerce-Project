from django.shortcuts import render
from django.views.generic.edit import UpdateView
from .models import *
from .forms import AddressForm,UserUpdateForm
from django.urls import  reverse_lazy
# Create your views here.


class UpdateAddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'update_address.html'
    success_url = reverse_lazy('index')


class UpdateUserProfile(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('index')


def index(request):
    return render(request,'index.html')




