from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.


def home_page(request):
    category = Category.objects.filter(parent=None)
    if request.GET.get('search'):
        category = category.filter(name__icontains=request.GET.get('search'))
    product = Product.objects.all()
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))

    return render(request, 'index.html', {'categorydata': category, 'productdata': product})


def category_data(request):
    category = Category.objects.filter(parent=None)
    if request.GET.get('search'):
        category = category.filter(name__icontains=request.GET.get('search'))
    p = Paginator(category, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'user_product/category.html', {'categorydata': page_obj})


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
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    p = Paginator(product, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'user_product/all_product.html', {'productdata': page_obj})
