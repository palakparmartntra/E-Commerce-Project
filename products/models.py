from django.db import models


class Brand(models.Model):
    """ this model contains details of products brand """

    name = models.CharField(max_length=40, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='static/img/brand')

    def __str__(self):
        return self.name


class Category(models.Model):
    """ this model contains details of product category """

    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='static/img/category')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ this model contains all product details """

    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField()
    quantity = models.IntegerField()
    price = models.CharField(max_length=100000)
    image = models.ImageField(upload_to='static/img/product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
