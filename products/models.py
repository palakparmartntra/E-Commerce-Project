from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from accounts.models import User


class Category(models.Model):
    """ this model contains details of product category """

    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='media/category')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    section_items = GenericRelation('SectionItems')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """ this model contains all product details """

    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='media/product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    section_items = GenericRelation('SectionItems')

    def __str__(self):
        return str(self.name)


class Brand(models.Model):
    """ this model contains details of products brand """

    name = models.CharField(max_length=40, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='media/brand')
    product = models.ManyToManyField(Product, through='BrandProduct')
    section_items = GenericRelation('SectionItems')

    def __str__(self):
        return str(self.name)


class BrandProduct(models.Model):
    """ this models is through table for brand and product """

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class SectionItems(models.Model):
    """ this model contains details of all the items in a section """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.content_type} - {self.object_id} - {self.content_object}'


class Section(models.Model):
    """ this model contains details of a section """

    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    section_items = models.ManyToManyField(SectionItems, through='SectionSectionItemsThrough')
    section_file = models.FileField(upload_to='media/section_files/', null=True)

    def __str__(self):
        return f'{self.name} - priority: {self.order}'


class SectionSectionItemsThrough(models.Model):
    """ this is an intermediate model between section and section items """

    section_items = models.ForeignKey(SectionItems, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f'section items: {self.section_items} - section: {self.section}'


class Banner(models.Model):
    """ this model contains banner details """

    banner_name = models.CharField(max_length=50, null=True, blank=True)
    banner_image = models.FileField(upload_to='media/banner', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_date']

    def __str__(self):
        return f'{self.banner_name}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.product}'


