from django.db.models import Count
from .forms import AddCategoryForm
from .models import Category, Brand, Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .headings import AdminPortalHeadings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required
def add_product(request):
    """ this view is useful to add products """

    context = {}
    if request.method == "POST":
        product = AddProductForm(request.POST, request.FILES)
        if product.is_valid():
            product.save()
            messages.success(request, AdminPortalHeadings.PRODUCT_ADDED)
        return redirect('view-product')

    product = AddProductForm()
    context['form'] = product
    context['heading'] = '  Add Products'
    return render(request, "product/products/add_products.html", context)


@login_required
def update_product(request, pk):
    """ this view is useful for update product product """

    context = {}
    product_instance = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product = AddProductForm(request.POST, request.FILES, instance=product_instance)
        if product.is_valid():
            product.save()
            messages.success(request, AdminPortalHeadings.PRODUCT_UPDATED)
        return redirect('view-product')

    product = AddProductForm(instance=product_instance)
    context['form'] = product
    context['heading'] = ' Update Product'
    return render(request, "product/products/update_products.html", context)


@login_required
def view_product(request):
    """ this view is useful to display all product """

    product = Product.objects.filter(is_deleted=False)
    print(product)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    p = Paginator(product, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'product/products/view_products.html',
                  {'page_obj': page_obj, 'heading': 'All Products'})


@login_required
def delete_product(request, pk):
    """ this view is useful to delete product """

    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, AdminPortalHeadings.PRODUCT_DELETED)
        return redirect('trashview')
    else:
        return render(request, 'product/products/confirm_delete.html', {'product': product})


@login_required
def trash_product(request):
    """ this view is useful to view all trash products """

    product = Product.objects.filter(is_deleted=True)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    p = Paginator(product, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'product/products/trash_product.html',
                  {'page_obj': page_obj, 'heading': 'Trash Products'})


@login_required
def soft_delete(request, pk):
    """ this view is useful to for soft delete and product goes to trash """
    product = Product.objects.get(id=pk)
    product.is_deleted = True
    product.save()
    return redirect('view-product')


@login_required
def restore(request, pk):
    """ this view is useful to restore product from trash """

    product = Product.objects.get(id=pk)
    product.is_deleted = False
    product.save()
    return redirect('trashview')


# Create your views here.
@login_required
def add_category(request):
    """ this view is useful to add category """

    context = {}
    if request.method == "POST":
        category = AddCategoryForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
            messages.success(request, AdminPortalHeadings.PRODUCT_ADDED)
        return redirect('view-category')

    category = AddCategoryForm()
    context['form'] = category
    context['heading'] = '  Add Categories'
    return render(request, "product/category/add_category.html", context)


@login_required
def update_category(request, pk):
    """ this view is useful for update product category """

    context = {}
    category_instance = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category = AddCategoryForm(request.POST, request.FILES, instance=category_instance)
        if category.is_valid():
            category.save()
            messages.success(request, AdminPortalHeadings.PRODUCT_UPDATED)
        return redirect('view-category')

    category = AddCategoryForm(instance=category_instance)
    context['form'] = category
    context['heading'] = ' Update Category'
    return render(request, "product/category/update_category.html", context)


@login_required
def view_categroy(request):
    """ this view is useful to display all categories """

    category = Category.objects.all()
    if request.GET.get('search'):
        category = category.filter(name__icontains=request.GET.get('search'))
    p = Paginator(category, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'product/category/view_category.html',
                  {'page_obj': page_obj, 'heading': 'All Categories'})


@login_required
def delete_category(request, pk):
    """ this view is useful to delete category """

    categorydata = get_object_or_404(Category, pk=pk)
    if request.method == "POST":

        categorydata.delete()
        messages.success(request, AdminPortalHeadings.PRODUCT_DELETED)
        return redirect('view-category')
    else:
        return render(request, 'product/category/confirm_delete.html', {'category': categorydata})


@login_required
def home_page(request):
    """" To redirect user to home page and superuser to dashboard """

    context = {}
    if not request.user.is_superuser:
        return render(request, "index.html")

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
