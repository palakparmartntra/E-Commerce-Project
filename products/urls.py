from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import home_page


urlpatterns = [
    path('', home_page, name='homepage'),
    path('profile/', home_page, name='admin-profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
