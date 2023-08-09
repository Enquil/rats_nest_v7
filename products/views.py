from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Category, Brand, Product, Domain
from django.views import View


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'domain' in request.GET:
            products = products.filter(domain=request.GET['domain'])

        if 'category' in request.GET:
            products = products.filter(category=request.GET['category'])

        if 'q' in request.GET:
            query = request.GET['q']

            if not query:
                messages.error(request, 'You didnt enter any search criteria')
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ Detailed view for chosen product """

    product = get_object_or_404(Product, pk=product_id)

    # Check if product has sizes
    if product.has_sizes:
        # If shoes
        if product.category.name == 'shoes':
            size_list = (
                '35', '36', '37', '38', '39', '40',
                '41', '42', '43', '44', '45', '46'
            )
        # If not shoes
        else:
            size_list = ('XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL')

    context = {
        'product': product,
        'size_list': size_list,
    }

    return render(request, 'products/product_detail.html', context)
