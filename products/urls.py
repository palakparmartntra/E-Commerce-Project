from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import product_detail

urlpatterns = [
    path('product/<int:product_pk>/<int:brand_pk>/', product_detail, name='product-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
