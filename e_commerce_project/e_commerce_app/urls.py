from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('index',views.main,name='index'),
    path('prodcut_details',views.product_details,name='product_details')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)