from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import add_brand, update_brands, view_brands, delete_brand

urlpatterns = [

    path('view-brand/', view_brands, name='view-brand'),
    path('add-brand', add_brand, name='add-brand'),
    path('update-brand/<int:pk>/', update_brands, name='update-brand'),
    path('delete-brand/<int:pk>/', delete_brand, name='delete-brand'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
