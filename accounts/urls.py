
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
                  path('', include('allauth.urls')),
                  path('', views.HomePageView.as_view(), name='homepage'),
                  path('addaddress/<int:pk>/', views.AddAddress.as_view(), name='add-address'),
                  path('index', views.Index.as_view(), name='index'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
