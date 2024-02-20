from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Category, Brand, Product
from .forms import AddBrandForm, UpdateBrandForm, AddCategoryForm, AddProductForm
from django.contrib import messages
from .messages import BrandFormSuccessMessages, BrandFormErrorMessages
from .exceptions import CannotDeleteBrandException
from django.contrib.auth.decorators import login_required
from .headings import AdminPortalHeadings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def add_product(request):
    """ this view is useful to add products """

    if not request.user.is_superuser:
        raise Http404

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

    if not request.user.is_superuser:
        raise Http404

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

    if not request.user.is_superuser:
        raise Http404

    product = Product.objects.filter(is_deleted=False)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    page = Paginator(product, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'product/products/view_products.html',
                  {'page_obj': page_obj, 'heading': 'All Products'})


@login_required
def delete_product(request, pk):
    """ this view is useful to delete product """

    if not request.user.is_superuser:
        raise Http404

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

    if not request.user.is_superuser:
        raise Http404

    product = Product.objects.filter(is_deleted=True)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    page = Paginator(product, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, 'product/products/trash_product.html',
                  {'page_obj': page_obj, 'heading': 'Trash Products'})


@login_required
def soft_delete(request, pk):
    """ this view is useful to for soft delete and product goes to trash """

    if not request.user.is_superuser:
        raise Http404

    product = Product.objects.get(id=pk)
    product.is_deleted = True
    product.save()
    return redirect('view-product')


@login_required
def restore(request, pk):
    """ this view is useful to restore product from trash """

    if not request.user.is_superuser:
        raise Http404

    product = Product.objects.get(id=pk)
    product.is_deleted = False
    product.save()
    return redirect('trashview')


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


@login_required
def add_category(request):
    """ this view is useful to add category """

    if not request.user.is_superuser:
        raise Http404

    context = {}
    if request.method == "POST":
        category = AddCategoryForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
            messages.success(request, AdminPortalHeadings.CATEGORY_ADDED)
        return redirect('view-category')

    category = AddCategoryForm()
    context['form'] = category
    context['heading'] = '  Add Categories'
    return render(request, "product/category/add_category.html", context)


@login_required
def update_category(request, pk):
    """ this view is useful for update product category """

    if not request.user.is_superuser:
        raise Http404

    context = {}
    category_instance = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category = AddCategoryForm(request.POST, request.FILES, instance=category_instance)
        if category.is_valid():
            category.save()
            messages.success(request, AdminPortalHeadings.CATEGORY_UPDATED)
        return redirect('view-category')

    category = AddCategoryForm(instance=category_instance)
    context['form'] = category
    context['heading'] = ' Update Category'
    return render(request, "product/category/update_category.html", context)


@login_required
def view_categroy(request):
    """ this view is useful to display all categories """

    if not request.user.is_superuser:
        raise Http404

    category = Category.objects.all()
    search = request.GET.get('search')
    if search is None:
        search = ""
    if search:
        if search is not None:
            category = category.filter(Q(name__icontains=search) | Q(parent__name__icontains=search))
        else:
            category = category.all()
    page = Paginator(category, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'product/category/view_category.html',
                  {'page_obj': page_obj, 'heading': AdminPortalHeadings.CATEGORY_HEADING, 'search': search})


@login_required
def delete_category(request, pk):
    """ this view is useful to delete category """

    if not request.user.is_superuser:
        raise Http404

    categorydata = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        product = Product.objects.filter(category=pk)
        try:
            if not product:
                categorydata.delete()
                messages.success(request, AdminPortalHeadings.CATEGORY_DELETED)
            else:
                raise CannotDeleteBrandException
        except CannotDeleteBrandException:
            messages.error(request, AdminPortalHeadings.CATEGORY_NOT_DELETED)
        return redirect('view-category')
    else:
        return render(request, 'product/category/delete_confirmation.html', {'category': categorydata,
                                        'heading': AdminPortalHeadings.CATEGORY_DELETE_HEADING})


@login_required
def add_brand(request):
    """ To add a new brand in brand model """

    if not request.user.is_superuser:
        raise Http404

    context = {}
    if request.method == "POST":
        brand = AddBrandForm(request.POST, request.FILES)
        if brand.is_valid():
            brand.save()
            messages.success(request, BrandFormSuccessMessages.NEW_BRAND_ADDED)
        return redirect('view-brand')

    brand_form = AddBrandForm()

    context = {
        "form": brand_form,
        "heading": AdminPortalHeadings.ADD_BRAND
    }
    return render(request, "product/brand/add_brand.html", context)


@login_required
def update_brands(request, pk):
    """ To update brand details """

    if not request.user.is_superuser:
        raise Http404

    context = {}

    selected_brand = get_object_or_404(Brand, id=pk)
    if request.method == "POST":
        brand_form = UpdateBrandForm(
            request.POST, request.FILES, instance=selected_brand
        )
        if brand_form.is_valid():
            brand_form.save()
            messages.success(request, BrandFormSuccessMessages.BRAND_UPDATED)
        return redirect('view-brand')

    brand_form = UpdateBrandForm(instance=selected_brand)

    context = {
        "form": brand_form,
        "heading": AdminPortalHeadings.UPDATE_BRAND
    }

    return render(request, "product/brand/update_brand.html", context)


@login_required
def view_brands(request):
    """ To display all brands """

    if not request.user.is_superuser:
        raise Http404

    brand = Brand.objects.all()
    search = request.GET.get('search')
    if search is None:
        search = ""
    if search:
        brand = brand.filter(name__icontains=request.GET.get('search'))
    else:
        brand = brand

    page = Paginator(brand, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    context = {
        'page_obj': page_obj,
        'heading': AdminPortalHeadings.ALL_BRANDS,
        'search': search
    }
    return render(request, 'product/brand/view_brands.html', context)


@login_required
def delete_brand(request, pk):
    """ To delete a brand from model """

    if not request.user.is_superuser:
        raise Http404

    brand = Brand.objects.get(id=pk)
    heading = AdminPortalHeadings.DELETE_BRAND

    if request.method == "POST":
        try:
            if not brand.product.exists():
                brand.delete()
            else:
                raise CannotDeleteBrandException
        except CannotDeleteBrandException:
            messages.error(request, BrandFormErrorMessages.BRAND_PROTECTED)
        return redirect('view-brand')
    else:
        context = {
            'heading': heading,
            'brand': brand
        }
        return render(request, 'product/brand/confirm_delete.html', context)
