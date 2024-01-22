from django.shortcuts import render, redirect
from allauth.account.forms import LoginForm, ResetPasswordForm
from allauth.account.views import LogoutView
from django.views.generic import UpdateView
from .models import *
from .forms import *


# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def my_account(request):
    return render(request, 'my-account.html')

