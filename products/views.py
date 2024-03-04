from django.shortcuts import render
from .models import Product, Category, BrandProduct


def product_detail(request, product_pk):
    """ Show details of a product """

    product = Product.objects.get(is_deleted=False, is_active=True, id=product_pk)
    brand_of_product = BrandProduct.objects.get(product=product_pk)
    categories = Category.objects.filter(parent=None)

    context = {
        "heading": product.name,
        "product": product,
        "categories": categories,
        "brand_of_product": brand_of_product
    }
    return render(request, 'user_product/product_details.html', context)
