from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .headings import AdminPortalHeadings
from .models import Brand, Product, Category, BrandProduct


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


def product_detail(request, product_pk, brand_pk):
    """ to show details of a product """

    product = Product.objects.get(is_deleted=False, is_active=True, id=product_pk)
    brand_of_product = BrandProduct.objects.get(product=product_pk, brand=brand_pk)
    categories = Category.objects.filter(parent=None)

    context = {
        "heading": product.name,
        "product": product,
        "categories": categories,
        "brand_of_product": brand_of_product
    }
    return render(request, 'user_product/product_details.html', context)
