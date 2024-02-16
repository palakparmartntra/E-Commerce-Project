from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home_page(request):
    """" To redirect user to home page and superuser to dashboard """

    category = Category.objects.filter(parent=None)
    product = Product.objects.all()
    if request.GET.get('search'):
        category = category.filter(name__icontains=request.GET.get('search'))
        product = product.filter(name__icontains=request.GET.get('search'))

    return render(request, 'index.html', {'categorydata': category, 'productdata': product})


def category_data(request):

    """" To Display all category data """

    category = Category.objects.filter(parent=None)
    if request.GET.get('search'):
        category = category.filter(name__icontains=request.GET.get('search'))
    page = Paginator(category, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'user_product/category.html', {'categorydata': page_obj})


def subcategory_data(request, pk):

    """ to display all the subcategory """

    id_parent = get_object_or_404(Category, pk=pk)
    subcategory = Category.objects.filter(parent=id_parent.pk)
    if request.GET.get('search'):
        subcategory = subcategory.filter(name__icontains=request.GET.get('search'))
    page = Paginator(subcategory, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, "user_product/subcategory.html", {'subcategorydata': page_obj})


def product_data(request, pk):

    """ to display of specific category Products """

    id_parent = get_object_or_404(Category, pk=pk)
    product = Product.objects.filter(category=id_parent.pk)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    page = Paginator(product, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'user_product/products.html', {'productdata': page_obj})


def all_products(request):

    """ to display all the Products """

    product = Product.objects.all()
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    page = Paginator(product, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, 'user_product/all_product.html', {'productdata': page_obj})
