from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCategoryForm
from .models import Category, Brand, Product
from .headings import AdminPortalHeadings
from .forms import AddBrandForm, UpdateBrandForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .messages import BrandFormSuccessMessages
from .messages import BrandFormErrorMessages
from .exceptions import CannotDeleteBrandException
from django.contrib.auth.decorators import login_required


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
def add_brand(request):
    """ To add a new brand in brand model """

    if not request.user.is_superuser:
        return Http404

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
        return Http404

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
        return Http404

    brand = Brand.objects.all()
    if request.GET.get('search'):
        brand = brand.filter(name__icontains=request.GET.get('search'))

    p = Paginator(brand, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj': page_obj,
        'heading': AdminPortalHeadings.ALL_BRANDS
    }
    return render(request, 'product/brand/view_brands.html', context)


@login_required
def delete_brand(request, pk):
    """ To delete a brand from model """

    if not request.user.is_superuser:
        return Http404

    brand = Brand.objects.get(id=pk)
    heading = AdminPortalHeadings.DELETE_BRAND

    if request.method == "POST":
        try:
            if not brand.product.exists():
                brand.delete()
            else:
                raise CannotDeleteBrandException
        except CannotDeleteBrandException:
            messages.info(request, BrandFormErrorMessages.BRAND_PROTECTED)
        return redirect('view-brand')
    else:
        context = {
            'heading': heading,
            'brand': brand
        }
        return render(request, 'product/brand/confirm_delete.html', context)
