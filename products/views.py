from django.shortcuts import render, redirect, get_object_or_404
from .models import Brand, BrandProduct
from .headings import AdminPortalHeadings
from .forms import AddBrandForm, UpdateBrandForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .messages import BrandFormSuccessMessages
from .messages import BrandFormErrorMessages
from .exceptions import CannotDeleteBrand
from django.contrib.auth.decorators import login_required


@login_required
def add_brand(request):
    """ To add a new brand in brand model """

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

    context = {}

    if request.method == "POST":
        brand_form = UpdateBrandForm(
            request.POST, request.FILES, instance=get_object_or_404(Brand, id=pk)
        )
        if brand_form.is_valid():
            brand_form.save()
            messages.success(request, BrandFormSuccessMessages.BRAND_UPDATED)
        return redirect('view-brand')

    brand_form = UpdateBrandForm(instance=Brand.objects.get(id=pk))

    context = {
        "form": brand_form,
        "heading": AdminPortalHeadings.UPDATE_BRAND
    }

    return render(request, "product/brand/update_brand.html", context)


@login_required
def view_brands(request):
    """ To display all brands """

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

    brand = Brand.objects.get(id=pk)
    product_has_brand = BrandProduct.objects.filter(brand=pk)
    heading = AdminPortalHeadings.DELETE_BRAND
    if request.method == "POST":
        try:
            if not product_has_brand:
                brand.delete()
            else:
                raise CannotDeleteBrand
        except CannotDeleteBrand:
            messages.info(request, BrandFormErrorMessages.BRAND_PROTECTED)
            breakpoint()
        return redirect('view-brand')
    else:
        context = {
            'heading': heading,
            'brand': brand
        }
        return render(request, 'product/brand/confirm_delete.html', context)
