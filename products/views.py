from django.shortcuts import render
from .models import Category,Product

# Create your views here.


def category_view(request):
    category = Category.objects.all()
    product = Product.objects.all()

    return render(request, 'index.html', {'categorydata': category, 'productdata': product})




