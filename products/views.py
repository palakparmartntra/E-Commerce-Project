import pandas as pd
from django.http import Http404
from django.contrib import messages
from .headings import AdminPortalHeadings
from .constants import SectionFormConstants
from .exceptions import CannotDeleteBrandException
from django.db.models import Q, Count, F, Case, When
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from .models import (Category, Brand, Product, BrandProduct, Banner,
                     Section, SectionItems)
from .forms import (AddBrandForm, UpdateBrandForm, AddCategoryForm,
                    AddProductForm, UpdateProductForm, AddBannerForm,
                    UpdateBannerForm, UpdateSectionForm, AddSectionForm)
from .messages import (BrandFormSuccessMessages, BrandFormErrorMessages,
                       SectionFormSuccessMessages)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home_page(request):
    """" To redirect user to home page """

    category = Category.objects.filter(parent=None)
    product = Product.objects.filter(is_active=True, is_deleted=False)
    banner_data = Banner.objects.filter(is_active=True)
    search = request.GET.get('search')
    if search:
        category = category.filter(name__icontains=search)
    if request.GET.get('search'):
        category = category.filter(name__icontains=search)
        product = product.filter(name__icontains=search)

    return render(request, 'index.html', {'categorydata': category, 'productdata': product,
                                          'banner_data': banner_data})


def dashboard(request):
    """" To redirect admin to dashboard """

    if not request.user.is_superuser:
        raise Http404

    banner = Banner.objects.annotate(banner_count=Count("banner_name")).all()
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
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))

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
        return render(request, 'product/category/delete_confirmation.html', {'category': categorydata,
                                                                             'heading': AdminPortalHeadings.CATEGORY_DELETE_HEADING})


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
        brand = brand.filter(name__icontains=search)
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


def category_data(request):
    """" To Display all category data """

    category = Category.objects.filter(parent=None)
    if request.GET.get('search'):
        category = category.filter(name__icontains=request.GET.get('search'))
    page = Paginator(category, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'user_product/category.html', {'categorydata': page_obj})


def subcategory_data(request, pk):
    """ to display all the subcategory """

    id_parent = get_object_or_404(Category, pk=pk)
    subcategory = Category.objects.filter(parent=id_parent.pk)
    if request.GET.get('search'):
        subcategory = subcategory.filter(name__icontains=request.GET.get('search'))
    page = Paginator(subcategory, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, "user_product/subcategory.html", {'subcategorydata': page_obj})


def product_data(request, pk):
    """ to display of specific category Products """

    id_parent = get_object_or_404(Category, pk=pk)
    product = Product.objects.filter(category=id_parent.id, is_active=True, is_deleted=False)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    page = Paginator(product, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    return render(request, 'user_product/products.html', {'productdata': page_obj})


def all_products(request):
    """ to display all the Products """

    product = Product.objects.filter(is_active=True, is_deleted=False)
    if request.GET.get('search'):
        product = product.filter(name__icontains=request.GET.get('search'))
    page = Paginator(product, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, 'user_product/all_product.html', {'productdata': page_obj})


@login_required
def banner_view(request):
    """ This view is useful to show all banners """

    banner_data = Banner.objects.filter(is_active=True)
    search = request.GET.get('search')
    if search is None:
        search = ""
    if search:
        banner_data = banner_data.filter(banner_name__icontains=search)
    page = Paginator(banner_data, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)
    return render(request, 'product/banner/show_banner.html', {'banner_data': page_obj, 'search': search,
                                                               'banner': banner_data})


@login_required
def add_banner(request):
    """ This view is useful to create banner """

    if request.method == "POST":
        form_data = AddBannerForm(request.POST, request.FILES)
        if form_data.is_valid():
            form_data.save()
        return redirect('banner')
    form_data = AddBannerForm()
    return render(request, 'product/banner/add_banner.html', {'form': form_data})


@login_required
def update_banner(request, pk):
    """This view is useful to update banner"""

    banner_data = get_object_or_404(Banner, id=pk)
    if request.method == "POST":
        form_data = UpdateBannerForm(request.POST, request.FILES, instance=banner_data)
        if form_data.is_valid():
            form_data.save()
        return redirect('banner')
    form_data = UpdateBannerForm(instance=banner_data)
    return render(request, 'product/banner/update_banner.html', {'form': form_data})


@login_required
def delete_banner(request, pk):
    """ This view is useful to delete banner """

    banner_data = Banner.objects.get(id=pk)
    if request.method == "POST":
        banner_data.delete()
        return redirect('banner')
    return render(request, 'product/banner/delete_confirm.html', {'banner': banner_data})


@login_required
def view_sections(request, pk=None):
    """ to display all the sections """

    if not request.user.is_superuser:
        raise Http404

    sections = Section.objects.all().order_by('order')

    search = request.GET.get('search')
    if search is None:
        search = ""
    if search:
        sections = Section.objects.filter(Q(name__icontains=search) | Q(order__icontains=search)
                                          | Q(is_active__icontains=search))
    else:
        sections = sections

    page = Paginator(sections, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)
    except PageNotAnInteger:
        page_obj = page.page(1)
    except EmptyPage:
        page_obj = page.page(page.num_pages)

    context = {
        'page_obj': page_obj,
        'heading': AdminPortalHeadings.SECTIONS,
        'search': search
    }
    return render(request, 'section/view_section.html', context)


@login_required
def update_section(request, pk):
    """
    To update section details:

    It updates Section Name, Order and File Uploaded
    Reads old file and new file uploaded in the section item related to section, compares them both
    Deletes the section items not present in file, ignores already created ones and creates remaining one

    """

    if not request.user.is_superuser:
        raise Http404

    context = {}

    selected_section = get_object_or_404(Section, id=pk)

    # To fetch
    content_type_model = Section.objects.get(id=pk).section_items.values_list('content_type', flat=True).first()
    model = ContentType.objects.values_list('model', flat=True).get(id=content_type_model)

    if request.method == "POST":
        section_form = UpdateSectionForm(
            request.POST, request.FILES, instance=selected_section
        )
        selected_file = selected_section.section_file
        file_content = pd.read_excel(selected_file)
        old_data_list = []
        for old_data in file_content.values:
            old_data_list.append(*old_data)

        if section_form.is_valid():
            if request.FILES:

                # To read the previously uploaded Excel file and create a list of ids in file

                uploaded_file = request.FILES['section_file']
                update_data = pd.read_excel(uploaded_file)
                new_data_list = []
                for new_data in update_data.values:
                    new_data_list.append(*new_data)

            old_data_set = set(old_data_list)
            new_data_set = set(new_data_list)
            breakpoint()
            to_delete_data = list(old_data_set.difference(new_data_set))
            to_create_data = list(new_data_set.difference(old_data_set))

            section_item_to_delete = SectionItems.objects.filter(object_id__in=to_delete_data)
            section_item_to_delete.delete()

            section_item_list = []
            for create_data in to_create_data:
                section_item = SectionItems(object_id=create_data, content_type_id=content_type_model)
                print(section_item)
                section_item_list.append(section_item)
                section_item.save()
            section_id = Section.objects.values_list('id', flat=True).order_by('-id')[0]
            last_created_section = Section.objects.get(id=section_id)
            last_created_section.section_items.add(*section_item_list)

            section_form.save()
            messages.success(request, SectionFormSuccessMessages.SECTION_UPDATED)
        return redirect('view-section')

    section_form = UpdateSectionForm(instance=selected_section)

    context = {
        "form": section_form,
        "heading": AdminPortalHeadings.UPDATE_SECTIONS,
        "model": model
    }
    return render(request, "section/update_section.html", context)


@login_required
def add_section(request):
    """ To add a new section in section model """

    if not request.user.is_superuser:
        raise Http404

    context = {}
    if request.method == "POST":
        section_form = AddSectionForm(request.POST, request.FILES)
        name = request.POST.get('name')
        order = request.POST.get('order')
        section_file = request.FILES.get('section_file')
        model = request.POST.get('content_type')

        model_id = ContentType.objects.values_list(
            'id', flat=True
        ).filter(app_label=SectionFormConstants.APP_LABEL, model=model)
        Section.objects.create(name=name, order=order,
                               section_file=section_file)

        uploaded_file = request.FILES['section_file']
        file_content = pd.read_excel(uploaded_file)
        section_item_object = []
        for index, ids in file_content.iterrows():
            section_item = SectionItems(object_id=ids, content_type_id=model_id[0])
            section_item_object.append(section_item)
            section_item.save()

        section_id = Section.objects.values_list('id', flat=True).order_by('-id')[0]
        last_created_section = Section.objects.get(id=section_id)
        last_created_section.section_items.add(*section_item_object)
        last_created_section.save()
        messages.success(request, SectionFormSuccessMessages.NEW_SECTION_ADDED)
        return redirect('view-section')

    section_form = AddSectionForm()
    context = {
        "section_form": section_form,
        "heading": AdminPortalHeadings.ADD_SECTION
    }
    return render(request, "section/add_section.html", context)
