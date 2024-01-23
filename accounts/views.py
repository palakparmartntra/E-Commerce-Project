from django.shortcuts import render, redirect

from .models import User
from django.views.generic import TemplateView

class HomePageView(TemplateView):

    template_name = 'index.html'












