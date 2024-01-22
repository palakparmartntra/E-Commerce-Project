from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User


def homepage(request):
    return render(request, 'index.html')

def my_account(request):
    return render(request, 'my-account.html')










