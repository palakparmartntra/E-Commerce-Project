from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import home_page
from .views import add_category, update_category, view_categroy, delete_category
from .views import add_brand, update_brands, view_brands, delete_brand


urlpatterns = [
    path('', home_page, name='homepage'),
    path('profile/', home_page, name='admin-profile'),
    path('addcategory', add_category, name='add-category'),
    path('updatecategory/<int:pk>/', update_category, name='update-category'),
    path('viewcategory/', view_categroy, name='view-category'),
    path('deletecategory/<int:pk>/', delete_category, name='delete-category'),
    path('view-brand/', view_brands, name='view-brand'),
    path('add-brand/', add_brand, name='add-brand'),
    path('update-brand/<int:pk>/', update_brands, name='update-brand'),
    path('delete-brand/<int:pk>/', delete_brand, name='delete-brand'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
