from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import  views

from allauth.account.views import LoginView

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('my_account/',views.my_account,name='my_accounts'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
