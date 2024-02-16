from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import home_page
from .views import add_product, update_product, view_product, delete_product, \
    trash_product, soft_delete, restore
from .views import add_category, update_category, view_categroy, delete_category
from .views import add_brand, update_brands, view_brands, delete_brand
from .views import category_data, subcategory_data, product_data, all_products
from .views import product_detail


urlpatterns = [
    path('', home_page, name='homepage'),
    path('profile/', home_page, name='admin-profile'),
    path('addproduct', add_product, name='add-product'),
    path('updateproduct/<int:pk>/', update_product, name='update-product'),
    path('viewproduct/', view_product, name='view-product'),
    path('deleteproduct/<int:pk>/', delete_product, name='delete-product'),
    path('trashproduct', trash_product, name='trashview'),
    path('softdelete/<int:pk>/', soft_delete, name='trash-product'),
    path('restore/<int:pk>/', restore, name='restore'),
    path('addcategory', add_category, name='add-category'),
    path('updatecategory/<int:pk>/', update_category, name='update-category'),
    path('viewcategory/', view_categroy, name='view-category'),
    path('deletecategory/<int:pk>/', delete_category, name='delete-category'),
    path('view-brand/', view_brands, name='view-brand'),
    path('add-brand/', add_brand, name='add-brand'),
    path('update-brand/<int:pk>/', update_brands, name='update-brand'),
    path('delete-brand/<int:pk>/', delete_brand, name='delete-brand'),
    path('category', category_data, name='category'),
    path('subcategory/<int:pk>/', subcategory_data, name='subcategory'),
    path('product/<int:pk>/', product_data, name='products'),
    path('allproducts/', all_products, name='all-products'),
    path('product/<int:product_pk>/<int:brand_pk>/', product_detail, name='product-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
