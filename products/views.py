from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Min
from .models import Product, Category, Tag
from cart.models import Cart, CartItem

def get_cart(request):
    from cart.views import get_cart as cart_get_cart
    return cart_get_cart(request)

def product_list(request):
    search_query = request.GET.get('q', '')
    category_ids = request.GET.getlist('category')
    tag_ids = request.GET.getlist('tag')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 1000000)
    rating = request.GET.get('rating', 0)
    sort = request.GET.get('sort', 'newest')

    products = Product.objects.filter(is_available=True)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_ids:
        products = products.filter(categories__id__in=category_ids).distinct()

    if tag_ids:
        products = products.filter(tags__id__in=tag_ids).distinct()

    if min_price or max_price:
        try:
            products = products.filter(packagings__isnull=False).annotate(
                min_price=Min('packagings__price')
            ).filter(
                min_price__gte=float(min_price),
                min_price__lte=float(max_price)
            )
        except ValueError:
            products = products.filter(packagings__isnull=False)

    if rating:
        try:
            products = products.filter(rating__gte=float(rating))
        except ValueError:
            pass

    if sort == 'popular':
        products = products.order_by('-sales_count')
    elif sort == 'price-low':
        products = products.filter(packagings__isnull=False).annotate(
            min_price=Min('packagings__price')
        ).order_by('min_price')
    elif sort == 'price-high':
        products = products.filter(packagings__isnull=False).annotate(
            min_price=Min('packagings__price')
        ).order_by('-min_price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    cart = get_cart(request)
    cart_count = cart.items.count()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'products/product_list.html', {
        'products': page_obj,
        'categories': categories,
        'tags': tags,
        'cart_count': cart_count,
        'search_query': search_query,
        'selected_categories': category_ids,
        'selected_tags': tag_ids,
        'min_price': min_price,
        'max_price': max_price,
        'rating': rating,
        'sort': sort,
        'page_obj': page_obj,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        categories__in=product.categories.all()
    ).exclude(pk=pk).distinct()[:4]
    cart = get_cart(request)
    cart_count = cart.items.count()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_count': cart_count,
    })