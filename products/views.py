from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Brand
from .headings import AdminPortalHeadings
from .forms import AddBrandForm, UpdateBrandForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .messages import BrandFormSuccessMessages, BrandFormErrorMessages
from .exceptions import CannotDeleteBrandException
from django.contrib.auth.decorators import login_required


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
