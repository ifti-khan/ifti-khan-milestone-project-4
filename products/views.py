from django.shortcuts import render
from .models import Product

# Create your views here.


def all_products(request):
    """
    A view to show all products on the products page,
    and this also includes sorting products and searching
    for products.
    """
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
