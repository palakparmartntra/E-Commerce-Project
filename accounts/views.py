from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """ view for rendering index page"""

    template_name = 'index.html'
