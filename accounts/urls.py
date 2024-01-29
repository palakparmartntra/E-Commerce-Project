from django.urls import path
from . import views

urlpatterns = [
    path('updateaddress/<int:pk>/', views.UpdateAddressView.as_view(), name='updateaddress'),
    path('updateprofile/<int:pk>/', views.UpdateUserProfile.as_view(), name='updateprofile'),

    path('index', views.Index.as_view(), name='index')

]
