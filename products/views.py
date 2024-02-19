from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCategoryForm
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from products.headings import AdminPortalHeadings
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from products.exceptions import CannotDeleteBrandException


# Create your views here.
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
        return render(request, 'product/category/confirm_delete.html', {'category': categorydata,
                                        'heading': AdminPortalHeadings.CATEGORY_DELETE_HEADING})
