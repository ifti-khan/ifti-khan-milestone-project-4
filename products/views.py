from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """
    A view to show all products on the products page,
    and this also includes sorting products and searching
    for products.
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # This block of code check to see if sort is in request.get
        # then sets it to none and sortkey, then if a user sorts by name
        # the sortkey will be renamed to lower_name. Then the current list
        # is annotated with a new field.
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            # This is sort the categories by name instead of id
            if sortkey == 'category':
                sortkey = 'category__category_name'

            # This block of code checks to see if direction is in
            # request.get and checks to see if the direction is
            # descending and then orders the products using the
            # order by model method.
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # This block of code is checking if the request get exists,
        # then splits the at the commas to make a list and uses that
        # list to filter the products using the category name from the list
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__category_name__in=categories)
            categories = Category.objects.filter(category_name__in=categories)

    # This block of code is checking if the request get exists
    # and uses the search bar name search and assigns to var query
    # so that it can be used to search for a product within the
    # products db. A error message will display if no search word has
    # been entered and redirected back to the products page.
    if request.GET:
        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(
                    request, "Please type something to search")
                return redirect(reverse('products'))

            # This block of code uses the user search query and finds
            # a match to the search query in both the
            # product name and description which is case insensitive
            queries = Q(product_name__icontains=query) | Q(
                product_description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    # context dictionary with keys and values to be
    # used in the rendered html template
    context = {
        'products': products,
        'product_search': query,
        'current_categories': categories,
        'current_sorting': current_sorting
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """
    A view to show individual product details
    when a product card is clicked on
    """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_details.html', context)


def add_product(request):
    """ Add a product to the store """
    # Checking if request is post for the form and request files for
    # the image file, which then checks to see if the form is valid, and
    # if so then save the form.
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Message that will inform the admin saying product successfully
            # added and returns the admin back to the add product page.
            messages.success(request, 'Product successfully added')
            return redirect(reverse('add_product'))
        else:
            # Error message to admin if product fails to add
            messages.error(request, 'Product failed to add,\
                Please make sure the form is correctly filled in.')
    else:
        form = ProductForm()

    # context dictionary with keys and values to be
    # used in the rendered html template
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
