from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('', views.HomePageView.as_view(), name='homepage'),
    path('profile/<str:username>/', views.profile, name='view_profile'),
    path('update-profile/<str:username>/', views.profile, name='update-profile'),
    path('update-address/<str:username>/<int:pk>/', views.profile, name='update-address'),
    path('add-address/<int:pk>/', views.AddAddress.as_view(), name='add-address'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
