from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('<pk>/', login_required(views.ViewProfile.as_view()), name='view_profile'),
    path('updateaddress/<int:pk>/', login_required(views.UpdateAddressView.as_view()), name='updateaddress'),
    path('updateprofile/<int:pk>/', login_required(views.UpdateUserProfile.as_view()), name='updateprofile'),
    path('addaddress/<int:pk>/', views.AddAddress.as_view(), name='add-address'),
    path('signup/', views.CustomSignupView.as_view(), name='account_signup'),

    path('index', views.Index.as_view(), name='index')

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
