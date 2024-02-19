from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddProductForm, UpdateProductForm
from .models import Product, BrandProduct, Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from products.headings import AdminPortalHeadings
from django.contrib.auth.decorators import login_required



@login_required
def add_product(request):
    """ this view is useful to add products """

    if not request.user.is_superuser:
        raise Http404

    context = {}
    if request.method == "POST":
        product = AddProductForm(request.POST, request.FILES)

        if product.is_valid():
            product_data = product.save()
            brand = product.cleaned_data['brand'].id
            selected_brand = get_object_or_404(Brand, id=brand)
            BrandProduct.objects.create(product=product_data, brand=selected_brand)
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
    brand = get_object_or_404(Brand, product=pk)
    brands_list = Brand.objects.all()

    if request.method == "POST":

        product = UpdateProductForm(request.POST, request.FILES, instance=product_instance)
        if product.is_valid():
            product.save()
            new_brand = request.POST.get('brand')
            BrandProduct.objects.filter(product=pk).update(brand=new_brand)
            messages.success(request, AdminPortalHeadings.PRODUCT_UPDATED)
        return redirect('view-product')

    product = UpdateProductForm(instance=product_instance)
    context['form'] = product
    context['brand'] = brand
    context['brands_list'] = brands_list
    context['heading'] = AdminPortalHeadings.PRODUCT_UPDATE_HEADING
    return render(request, "product/products/update_products.html", context)


@login_required
def view_product(request):
    """ this view is useful to display all product """
    if not request.user.is_superuser:
        raise Http404
    product = Product.objects.filter(is_deleted=False)

    search = request.GET.get('search')
    if search is None:
        search = ""
    if search:
        if search is not None:
            product = product.filter(Q(name__icontains=search) | Q(category__name__icontains=search)
                                     | Q(brand__name__icontains=search))
        else:
            product = product.all()
    page = Paginator(product, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'product/products/view_products.html',
                  {'page_obj': page_obj, 'heading': AdminPortalHeadings.PRODUCT_HEADING,
                   'search': search})


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
    search = request.GET.get('search')
    if search is None:
        search = ""
    if search:
        product = product.filter(Q(name__icontains=search) | Q(brand__name__icontains=search)
                                 | Q(category__name__icontains=search))
    else:
        product = product
    page = Paginator(product, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, 'product/products/trash_product.html',
                  {'page_obj': page_obj, 'heading': AdminPortalHeadings.PRODUCT_TRASH_HEADING,
                   'search': search})


@login_required
def soft_delete(request, pk):
    """ this view is useful to for soft delete and product goes to trash """

    if not request.user.is_superuser:
        raise Http404

    product = Product.objects.get(id=pk)
    product.is_deleted = True
    product.save()
    messages.info(request, AdminPortalHeadings.PRODUCT_MOVE_TO_TRASH)
    return redirect('view-product')


@login_required
def restore(request, pk):
    """ this view is useful to restore product from trash """

    if not request.user.is_superuser:
        raise Http404

    product = Product.objects.get(id=pk)
    product.is_deleted = False
    product.save()
    messages.success(request, AdminPortalHeadings.PRODUCT_RESTORED)
    return redirect('trashview')
