from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import add_category, update_category, view_categroy, delete_category

urlpatterns = [
    path('addcategory', add_category, name='add-category'),
    path('updatecategory/<int:pk>/', update_category, name='update-category'),
    path('viewcategory/', view_categroy, name='view-category'),
    path('deletecategory/<int:pk>/', delete_category, name='delete-category'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
