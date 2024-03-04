import pandas as pd
from functools import wraps
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from .headings import AdminPortalHeadings
from .constants import SectionFormConstants
from .exceptions import CannotDeleteBrandException, InvalidFileTypeException
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import (Category, Brand, Product, BrandProduct, Banner,
                     Section, SectionItems)
from .forms import (AddBrandForm, UpdateBrandForm, AddCategoryForm,
                    AddProductForm, UpdateProductForm, AddBannerForm,
                    UpdateBannerForm, UpdateSectionForm, AddSectionForm)
from .messages import (BrandFormSuccessMessages, BrandFormErrorMessages,
                       SectionFormSuccessMessages, SectionFormErrorMessages)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def home_page(request):
    """" To redirect user to home page """

    banner_data = Banner.objects.filter(is_active=True)
    category_data = Category.objects.all()
    section_data = Section.objects.filter(is_active=True)
    section_items_list = []
    section_name_list = []
    section_zip = zip(section_name_list, section_items_list)
    for section in section_data:
        section_content_type = section.section_items.values_list('content_type__model', flat=True).distinct()
        content_type = ContentType.objects.get(model=section_content_type[0])
        model = content_type.model_class()
        all_id = section.section_items.values_list('object_id', flat=True)
        section_items = model.objects.filter(id__in=all_id)
        section_name = section.name
        section_name_list.append(section_name)
        section_items_list.append(section_items)

    search = request.GET.get('search')
    if search:
        section_data = section_data.filter(name__icontains=search)
    return render(request, 'index.html', {'section_data': section_data, 'banner_data': banner_data,
                                          'section_zip': section_zip, 'category_data': category_data})


@login_required
@superuser_required
def dashboard(request):
    """" To redirect admin to dashboard """

    banner_count = Banner.objects.all().count()
    category_count = Category.objects.all().count()
    brand_count = Brand.objects.all().count()
    product_count = Product.objects.all().count()
    section_count = Section.objects.all().count()
    heading = AdminPortalHeadings.DASHBOARD

    context = {
        "heading": heading,
        "banner_count": banner_count,
        "category_count": category_count,
        "brand_count": brand_count,
        "product_count": product_count,
        "section_count": section_count
    }

    return render(request, "product/dashboard.html", context)


@login_required
@superuser_required
def add_product(request):
    """ this view is useful to add products """

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
@superuser_required
def update_product(request, pk):
    """ this view is useful for update product product """

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
@superuser_required
def view_product(request):
    """ this view is useful to display all product """

    product = Product.objects.filter(is_deleted=False)

    search = request.GET.get('search', "")
    if search:
        product = product.filter(
            Q(name__icontains=search) | Q(category__name__icontains=search)
            | Q(brand__name__icontains=search)
        )

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
@superuser_required
def delete_product(request, pk):
    """ this view is useful to delete product """

    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, AdminPortalHeadings.PRODUCT_DELETED)
        return redirect('trashview')
    else:
        return render(request, 'product/products/confirm_delete.html', {'product': product})


@login_required
@superuser_required
def trash_product(request):
    """ this view is useful to view all trash products """

    product = Product.objects.filter(is_deleted=True)
    search = request.GET.get('search', "")
    if search:
        product = product.filter(
            Q(name__icontains=search) | Q(brand__name__icontains=search)
            | Q(category__name__icontains=search)
        )

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
@superuser_required
def soft_delete(request, pk):
    """ this view is useful to for soft delete and product goes to trash """

    product = Product.objects.get(id=pk)
    product.is_deleted = True
    product.save()
    messages.info(request, AdminPortalHeadings.PRODUCT_MOVE_TO_TRASH)
    return redirect('view-product')


@login_required
@superuser_required
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
@superuser_required
def add_category(request):
    """ this view is useful to add category """

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
@superuser_required
def update_category(request, pk):
    """ this view is useful for update product category """

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
@superuser_required
def view_categroy(request):
    """ this view is useful to display all categories """

    category = Category.objects.all()
    search = request.GET.get('search', "")
    if search:
        category = category.filter(Q(name__icontains=search) | Q(parent__name__icontains=search))

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
@superuser_required
def delete_category(request, pk):
    """ this view is useful to delete category """

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
@superuser_required
def add_brand(request):
    """ To add a new brand in brand model """

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
@superuser_required
def update_brands(request, pk):
    """ To update brand details """

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
@superuser_required
def view_brands(request):
    """ To display all brands """

    brand = Brand.objects.all()
    search = request.GET.get('search', "")
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
@superuser_required
def delete_brand(request, pk):
    """ To delete a brand from model """

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
    search = request.GET.get('search', "")
    if search:
        category = category.filter(name__icontains=search)
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
    search = request.GET.get('search', "")
    if search:
        subcategory = subcategory.filter(name__icontains=search)

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
    search = request.GET.get('search', "")
    if search:
        product = product.filter(name__icontains=search)

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
    search = request.GET.get('search', "")
    if search:
        product = product.filter(name__icontains=search)

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
@superuser_required
def banner_view(request):
    """ This view is useful to show all banners """

    banner_data = Banner.objects.filter(is_active=True)
    search = request.GET.get('search', "")
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
@superuser_required
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
@superuser_required
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
@superuser_required
def delete_banner(request, pk):
    """ This view is useful to delete banner """

    banner_data = Banner.objects.get(id=pk)
    if request.method == "POST":
        banner_data.delete()
        return redirect('banner')
    return render(request, 'product/banner/delete_confirm.html', {'banner': banner_data})


@login_required
@superuser_required
def view_sections(request, pk=None):
    """ to display all the sections """

    sections = Section.objects.all().order_by('name')

    search = request.GET.get('search', "")
    if search:
        sections = sections.filter(
            Q(name__icontains=search) | Q(order__icontains=search)
            | Q(is_active__icontains=search)
        )

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
@superuser_required
def update_section(request, pk):
    """
    To update section details:

    It updates Section Name, Order and File Uploaded
    Reads old file and new file uploaded in the section item related to section, compares them both
    Deletes the section items not present in file, ignores already created ones and creates remaining one

    """

    selected_section = get_object_or_404(Section, id=pk)

    # Get ContentType model name of selected section
    content_type_model = Section.objects.get(id=pk).section_items.values_list('content_type', flat=True).first()

    # Get model name of fetched ContentType
    model = ContentType.objects.values_list('model', flat=True).get(id=content_type_model)

    if request.method == "POST":
        section_form = UpdateSectionForm(
            request.POST, request.FILES, instance=selected_section
        )

        # Read the content of the previously uploaded file
        selected_file = selected_section.section_file
        file_content = pd.read_excel(selected_file)
        old_data_list = []
        for old_data in file_content.values:
            old_data_list.append(*old_data)

        if section_form.is_valid():
            if request.FILES:

                # Read the uploaded Excel file
                uploaded_file = request.FILES['section_file']
                update_data = pd.read_excel(uploaded_file)
                new_data_list = []
                for new_data in update_data.values:
                    new_data_list.append(*new_data)

            old_data_set = set(old_data_list)
            new_data_set = set(new_data_list)

            # Create a list of ids to be deleted
            to_delete_data = list(old_data_set.difference(new_data_set))

            # Create a list of ids tp be created
            to_create_data = list(new_data_set.difference(old_data_set))

            # Get records to be deleted
            section_item_to_delete = SectionItems.objects.filter(object_id__in=to_delete_data)
            section_item_to_delete.delete()

            # Create new section items in SectionItems model
            section_item_list = []
            for create_data in to_create_data:
                section_item = SectionItems(object_id=create_data, content_type_id=content_type_model)
                section_item_list.append(section_item)
                section_item.save()

            section_form.save()

            #  Get last created section and add section items to many-to-many field
            section_id = Section.objects.values_list('id', flat=True).order_by('-id')[0]
            last_created_section = Section.objects.get(id=section_id)
            last_created_section.section_items.add(*section_item_list)

            messages.success(request, SectionFormSuccessMessages.SECTION_UPDATED)
        return redirect('view-section')

    # If the request method is not POST, render t he form
    section_form = UpdateSectionForm(instance=selected_section)

    context = {
        "form": section_form,
        "heading": AdminPortalHeadings.UPDATE_SECTIONS,
        "model": model
    }
    return render(request, "section/update_section.html", context)


@login_required
@superuser_required
def add_section(request):
    """
    To add a new section in section model.
    Creates a new section in section model

    """

    # Check if the request method is POST
    if request.method == "POST":
        name = request.POST.get('name')
        order = request.POST.get('order')
        section_file = request.FILES.get('section_file')
        model = request.POST.get('content_type')

        # Get the ContentType model instance
        model_instance = ContentType.objects.get(app_label=SectionFormConstants.APP_LABEL, model=model)

        # Create a new Section object
        Section.objects.create(name=name, order=order,
                               section_file=section_file)

        # Check the file extension
        uploaded_file = request.FILES['section_file']
        file_extension = uploaded_file.name.split(".")
        try:
            if file_extension[1] not in SectionFormConstants.valid_extensions:
                raise InvalidFileTypeException
        except InvalidFileTypeException:
            messages.error(request, SectionFormErrorMessages.INVALID_FILE_TYPE)
            return redirect(to='add-section')

        # Read the content of the uploaded file
        file_content = pd.read_excel(uploaded_file)
        section_item_object = []

        # Create SectionItems objects for each row in the file
        for index, ids in file_content.iterrows():
            section_item = SectionItems(object_id=ids, content_type=model_instance)
            section_item_object.append(section_item)
            section_item.save()

        # Add the SectionItems to the last created Section object
        section_id = Section.objects.values_list('id', flat=True).order_by('-id')[0]
        last_created_section = Section.objects.get(id=section_id)
        last_created_section.section_items.add(*section_item_object)
        last_created_section.save()

        # Display success message and redirect to view-section page
        messages.success(request, SectionFormSuccessMessages.NEW_SECTION_ADDED)
        return redirect('view-section')

    # If the request method is not POST, render the form
    section_form = AddSectionForm()
    context = {
        "section_form": section_form,
        "heading": AdminPortalHeadings.ADD_SECTION
    }
    return render(request, "section/add_section.html", context)


@login_required
@superuser_required
def update_section_status(request, pk):
    """
    To update the status of a section and return to view section page.
    """

    section = get_object_or_404(Section, id=pk)
    if pk:
        if section.is_active:
            section.is_active = False
        else:
            section.is_active = True
        section.save()
        return redirect(to='view-section')
