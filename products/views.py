from django.shortcuts import render
from .models import Product, Category


def product_detail(request, pk):
    """ to show details of a product """

    product = Product.objects.get(id=pk)
    categories = Category.objects.filter(parent=None)

    context = {
        "heading": product.name,
        "product": product,
        "categories": categories
    }
    return render(request, 'user_product/product_details.html', context)
