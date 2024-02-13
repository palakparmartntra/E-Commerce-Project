from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.


def category_view(request):
    category = Category.objects.filter(parent=None)
    product = Product.objects.all()

    return render(request, 'index.html', {'categorydata': category, 'productdata': product})


def category_data(request):
    category = Category.objects.filter(parent=None)
    return render(request, 'user_product/category.html', {'categorydata': category})


def subcategory_data(request, pk):
    id_parent = get_object_or_404(Category, pk=pk)
    print(id_parent)
    subcategory = Category.objects.filter(parent=id_parent.pk)
    return render(request, "user_product/subcategory.html", {'subcategorydata': subcategory})


def product_data(request, pk):
    id_parent = get_object_or_404(Category, pk=pk)
    product = Product.objects.filter(category=id_parent.pk)
    return render(request, 'user_product/products.html', {'productdata': product})


def all_products(request):
    product = Product.objects.all()
    return render(request, 'user_product/all_product.html', {'productdata': product})
