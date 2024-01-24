
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
                  path('', views.HomePageView.as_view(), name='homepage'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
