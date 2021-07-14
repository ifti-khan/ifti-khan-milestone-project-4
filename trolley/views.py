from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_trolley(request):
    """
    A view that renders the trolley page
    and its contents
    """

    return render(request, 'trolley/trolley.html')


def add_to_trolley(request, item_id):
    """
    Adding products with and without sizes and quantity specified by the user
    to the shopping trolley. It does this by getting the qty from the input
    element and converting it from string to int. Then it checks to see if the
    product posted has a size or not and is not already in the trolley session.
    if the product is already in the trolley the quantity will be incremented,
    or if its a new product it will be added to the shopping trolley. When a
    product is added to the shopping trolley the user will see a message
    informing them that the product has been added to the shopping trolley.
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('product_quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'clothing_sizes' in request.POST:
        size = request.POST['clothing_sizes']
    trolley = request.session.get('trolley', {})

    if size:
        if item_id in list(trolley.keys()):
            if size in trolley[item_id]['item_size'].keys():
                trolley[item_id]['item_size'][size] += quantity
                messages.success(
                    request, f'Size {size.upper()} - {product.product_name}\
                        quantity has been updated to\
                            {trolley[item_id]["item_size"][size]}')
            else:
                trolley[item_id]['item_size'][size] = quantity
                messages.success(
                    request, f'Size {size.upper()} -\
                        {product.product_name}, has been added to\
                            your shopping trolley')
        else:
            trolley[item_id] = {'item_size': {size: quantity}}
            messages.success(
                request, f'Size {size.upper()} -\
                        {product.product_name}, has been added to\
                            your shopping trolley')
    else:
        if item_id in list(trolley.keys()):
            trolley[item_id] += quantity
            messages.success(
                request, f'{product.product_name}\
                    quantity has been updated to {trolley[item_id]}')
        else:
            trolley[item_id] = quantity
            messages.success(
                request, f'{product.product_name}, has been added to\
                    your shopping trolley')

    request.session['trolley'] = trolley
    return redirect(redirect_url)


def adjust_trolley(request, item_id):
    """
    Adjusting the product quantity within the shopping trolley page,
    for products with sizes and products with no sizes. By checking if
    the product has a size and if the quantity is greater than zero then
    add to trolley or update if already in trolley the trolley and
    display a message to the user. Also if the value is zero and the quantity
    form is updated it will also remove the product from the shopping trolley.
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('product_quantity'))
    size = None
    if 'clothing_sizes' in request.POST:
        size = request.POST['clothing_sizes']
    trolley = request.session.get('trolley', {})

    if size:
        if quantity > 0:
            trolley[item_id]['item_size'][size] = quantity
            messages.success(
                request, f'Size {size.upper()} - {product.product_name}\
                    quantity has been updated to\
                        {trolley[item_id]["item_size"][size]}')
        else:
            del trolley[item_id]['item_size'][size]
            if not trolley[item_id]['item_size']:
                trolley.pop(item_id)
            messages.success(
                request, f'Size {size.upper()} -\
                    {product.product_name}, has been removed\
                from your shopping trolley')
    else:
        if quantity > 0:
            trolley[item_id] = quantity
            messages.success(
                request, f'{product.product_name}\
                    quantity has been updated to {trolley[item_id]}')
        else:
            trolley.pop(item_id)
            messages.success(
                request, f'{product.product_name}, has been removed\
                from your shopping trolley')

    request.session['trolley'] = trolley
    # Once the user updates the quantity they will
    # be taken back to the shopping trolley page
    return redirect(reverse('view_trolley'))


def remove_from_trolley(request, item_id):
    """
    Removing products with sizes and also products with no sizes from
    the shopping trolley by checking if the product has a size and then
    removing that specific item from the shopping trolley, or if no sizes
    then remove from the shopping trolley. Then display a message to the
    user on successful removal of product from the shopping trolley.
    """
    # Try block used to catch server errors and display an error message
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'clothing_sizes' in request.POST:
            size = request.POST['clothing_sizes']
        trolley = request.session.get('trolley', {})

        if size:
            del trolley[item_id]['item_size'][size]
            if not trolley[item_id]['item_size']:
                trolley.pop(item_id)
            messages.success(
                request, f'Size {size.upper()} - \
                    {product.product_name}, has been removed\
                from your shopping trolley')
        else:
            trolley.pop(item_id)
            messages.success(
                request, f'{product.product_name}, has been removed\
                from your shopping trolley')

        request.session['trolley'] = trolley
        # 200 terminal response on successful product removal from trolley
        return HttpResponse(status=200)

    # 500 terminal response if error removing product from trolley
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
