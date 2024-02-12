from django.shortcuts import render
from .models import Brand, Category, Product
from django.contrib import messages
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


@login_required
def profile(request):
    """" To show and update user details of the current user """

    if request.method == "POST":
        profile_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully")
    else:
        profile_form = UserUpdateForm(instance=User.objects.get(username=request.user))

    return render(request, 'profile/profile.html', {
        "profile_form": profile_form
    })

