from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import home_page, product_detail


urlpatterns = [
    path('', home_page, name='homepage'),
    path('profile/', home_page, name='admin-profile'),
    path('product/<int:product_pk>/<int:brand_pk>/', product_detail, name='product-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
