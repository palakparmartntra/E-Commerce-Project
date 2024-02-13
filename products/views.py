from django.shortcuts import render,redirect
from .models import Brand, Category, Product
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import AddCategoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.headings import AdminPortalHeadings


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

    category = AddCategoryForm(instance=Category.objects.get(id=pk))
    context['form'] = category
    context['heading'] = ' Update Category'
    return render(request, "product/category/update_category.html", context)


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


def delete_category(request, pk):
    """ this view is useful to delete category """

    categorydata = Category.objects.get(id=pk)
    if request.method == "POST":

        categorydata.delete()
        messages.success(request, AdminPortalHeadings.PRODUCT_DELETED)
        return redirect('view-category')
    else:
        return render(request, 'product/category/confirm_delete.html', {'category': categorydata})
