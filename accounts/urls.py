
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.HomePageView, name='homepage'),
    path('<pk>/', views.ViewProfile, name='view_profile'),
    path('updateaddress/<int:pk>/', views.UpdateAddressView, name='updateaddress'),
    path('updateprofile/<int:pk>/', views.UpdateUserProfile, name='updateprofile'),


    path('index', views.Index, name='index')

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
