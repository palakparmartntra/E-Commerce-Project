from django.contrib import admin
from .models import (Product, Category, Brand, BrandProduct,
                     Section, SectionItems, SectionSectionItemsThrough, Banner)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'quantity',
                    'price', 'image', 'category', 'is_active', 'is_deleted')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'parent')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')


@admin.register(BrandProduct)
class BrandProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'product')


@admin.register(SectionItems)
class SectionItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'content_object')


@admin.register(SectionSectionItemsThrough)
class SectionSectionItemsThroughAdmin(admin.ModelAdmin):
    list_display = ('section_items', 'section')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_name', 'banner_image', 'is_active', 'created_date', 'updated_date')


class SectionItemsInline(admin.TabularInline):
    model = SectionSectionItemsThrough
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'is_active', 'section_file')
    inlines = (SectionItemsInline,)
