from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
                  path('addproduct', add_product, name='add-product'),
                  path('updateproduct/<int:pk>/', update_product, name='update-product'),
                  path('viewproduct/', view_product, name='view-product'),
                  path('deleteproduct/<int:pk>/', delete_product, name='delete-product'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
