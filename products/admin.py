from django.contrib import admin
from .models import (Product, Category, Brand, BrandProduct,
                     Section, SectionItems, SectionSectionItemsThrough, Banner)


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity',
                    'price', 'image', 'category', 'is_active', 'is_deleted')


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'image', 'parent')


@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(BrandProduct)
class BrandProduct(admin.ModelAdmin):
    list_display = ('brand', 'product')


@admin.register(Section)
class Section(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'section_file')


@admin.register(SectionItems)
class SectionItems(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object')


@admin.register(SectionSectionItemsThrough)
class SectionSectionItemsThrough(admin.ModelAdmin):
    list_display = ('section_items', 'section')


@admin.register(Banner)
class Banner(admin.ModelAdmin):
    list_display = ('banner_name', 'banner_image', 'is_active', 'created_date', 'updated_date')
