from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCategoryForm
from .models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# Create your views here.
def add_category(request):
    """ this view is useful to add category """

    context = {}
    if request.method == "POST":
        category = AddCategoryForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
            messages.success(request, "category added successfully")
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
            messages.success(request, "category updated successfully")
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
        messages.success(request, "category deleted successfully")
        return redirect('view-category')
    else:
        return render(request, 'product/category/confirm_delete.html', {'category': categorydata})
