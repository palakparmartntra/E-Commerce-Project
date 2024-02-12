from django.shortcuts import render
from .models import Brand, Category, Product
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .headings import AdminPortalHeadings


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
