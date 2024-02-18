from django.db import models


class Category(models.Model):
    """ this model contains details of product category """

    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='static/media/category')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

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
    image = models.ImageField(upload_to='static/media/product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Brand(models.Model):
    """ this model contains details of products brand """

    name = models.CharField(max_length=40, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='static/media/brand')
    product = models.ManyToManyField(Product, through='BrandProduct')

    def __str__(self):
        return str(self.name)


class BrandProduct(models.Model):
    """ this models is through table for brand and product """

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
