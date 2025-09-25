from django.shortcuts import render
from products.models import Product

def home(request):
    popular_products = Product.objects.filter(is_available=True).order_by('-sales_count')[:4]
    return render(request, "root/index.html", {
        'popular_products': popular_products,
    })