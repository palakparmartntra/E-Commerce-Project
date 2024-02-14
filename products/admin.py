from django.contrib import admin

# Register your models here.
from .models import Product, Category, Brand, BrandProduct


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity', 'price', 'image', 'category'
                    , 'is_active', 'is_deleted')


@admin.register(Category)
class Categroy(admin.ModelAdmin):
    list_display = ('name', 'image', 'parent')


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(BrandProduct)
class BrandProduct(admin.ModelAdmin):
    list_display = ('brand', 'product')
