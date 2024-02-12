from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import HomePageView, profile, address, AddAddress

urlpatterns = [
    path('', include('allauth.urls')),
    # path('', HomePageView.as_view(), name='homepage'),
    path('profile/', profile, name='profile'),
    path('profile/update-address', address, name='address'),
    path('add-address/<int:pk>/', AddAddress.as_view(), name='add-address'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
