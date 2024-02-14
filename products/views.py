from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Brand, Category, Product
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .headings import AdminPortalHeadings


def home_page(request):
    """" To redirect user to home page and superuser to dashboard """

    context = {}
    if not request.user.is_superuser:
        category = Category.objects.filter(parent=None)
        if request.GET.get('search'):
            category = category.filter(name__icontains=request.GET.get('search'))
        product = Product.objects.all()
        if request.GET.get('search'):
            product = product.filter(name__icontains=request.GET.get('search'))

        return render(request, 'index.html', {'categorydata': category, 'productdata': product})

    else:
        banner = Brand.objects.annotate(banner_count=Count("name")).all()
        categories = Category.objects.annotate(catogory_count=Count("name")).all()
        brands = Brand.objects.annotate(brands_count=Count("name")).all()
        products = Product.objects.annotate(product_count=Count("name")).all()
        heading = AdminPortalHeadings.DASHBOARD

        context = {
            "heading": heading,
            "banner_count": banner,
            "categories_count": categories,
            "brands_count": brands,
            "products_count": products
        }

        return render(request, "product/dashboard.html", context)


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
    subcategory = Category.objects.filter(parent=id_parent.pk)
    if request.GET.get('search'):
        subcategory = subcategory.filter(name__icontains=request.GET.get('search'))
    p = Paginator(subcategory, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "user_product/subcategory.html", {'subcategorydata': page_obj})


def product_data(request, pk):
    id_parent = get_object_or_404(Category, pk=pk)
    product = Product.objects.filter(category=id_parent.pk)
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

    return render(request, 'user_product/products.html', {'productdata': page_obj})


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
