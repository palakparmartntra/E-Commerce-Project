from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import category_view, category_data,subcategory_data\
    ,product_data, all_products, home_page


urlpatterns = [
    path('', home_page, name='homepage'),
    path('profile/', home_page, name='admin-profile'),
    path('', category_view, name='user-category'),
    path('category', category_data, name='category'),
    path('subcategory/<int:pk>/', subcategory_data, name='subcategory'),
    path('product/<int:pk>/', product_data, name='products'),
    path('products/', all_products, name='all-products')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
