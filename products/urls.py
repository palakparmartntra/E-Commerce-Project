
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import category_view


urlpatterns = [
    path('', category_view, name='user-category'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
