from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from allauth.account.views import LoginView

urlpatterns = [
    path('',views.HomePageView.as_view(),name='homepage'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
