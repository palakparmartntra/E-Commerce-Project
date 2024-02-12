from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddProductForm
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def add_product(request):
    """ this view is useful to add products """

    context = {}
    if request.method == "POST":
        product = AddProductForm(request.POST, request.FILES)
        if product.is_valid():
            product.save()
        return redirect('view-product')

    product = AddProductForm()
    context['form'] = product
    context['heading'] = '  Add Products'
    return render(request, "product/products/add_products.html", context)


def update_product(request, pk):
    """ this view is useful for update product product """

    context = {}
    product_instance = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product = AddProductForm(request.POST, request.FILES, instance=product_instance)
        if product.is_valid():
            product.save()
        return redirect('view-product')

    product = AddProductForm(instance=Product.objects.get(id=pk))
    context['form'] = product
    context['heading'] = ' Update Product'
    return render(request, "product/products/update_products.html", context)


def view_product(request):
    """ this view is useful to display all product """

    product = Product.objects.all()
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

    return render(request, 'product/products/view_products.html', {'page_obj': page_obj, 'heading': 'All Products'})


def delete_product(request, pk):
    """ this view is useful to delete product """

    product = Product.objects.get(id=pk)
    if request.method == "POST":

        product.delete()
        return redirect('view-product')
    else:
        return render(request, 'product/products/confirm_delete.html', {'product': product})
