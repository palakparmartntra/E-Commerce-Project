from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import add_product, update_product, view_product, delete_product, \
    trash_product, soft_delete, restore, home_page

urlpatterns = [
    path('', home_page, name='homepage'),
    path('profile/', home_page, name='admin-profile'),
    path('addproduct', add_product, name='add-product'),
    path('updateproduct/<int:pk>/', update_product, name='update-product'),
    path('viewproduct/', view_product, name='view-product'),
    path('deleteproduct/<int:pk>/', delete_product, name='delete-product'),
    path('trashproduct', trash_product, name='trashview'),
    path('softdelete/<int:pk>/', soft_delete, name='trash-product'),
    path('restore/<int:pk>/', restore, name='restore')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
