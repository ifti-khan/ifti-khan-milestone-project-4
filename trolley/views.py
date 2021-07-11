from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.


def view_trolley(request):
    """
    A view that renders the trolley page
    and its contents
    """

    return render(request, 'trolley/trolley.html')


def add_to_trolley(request, item_id):
    """
    Adds a product quantity specified by the user
    to the shopping trolley
    """

    # This block of code gets the quantity from the form and coverts it
    # from string to integer.
    # It also gets the redirect url from the form and then creates a empty
    # trolley dictionary session if one has not already been created.
    quantity = int(request.POST.get('product_quantity'))
    redirect_url = request.POST.get('redirect_url')

    # This block of code initializes the size var to none and then checks
    # to see if the product sizes has been posted to the URL and then
    # sets size to the size selected from the URL
    size = None
    if 'clothing_sizes' in request.POST:
        size = request.POST['clothing_sizes']

    trolley = request.session.get('trolley', {})

    # This block of code will check to see if the same item with the same
    # size is in the trolley and if it is then the quantity will be incremented
    # and if not then set it to the quantity the user has chosen. This only
    # applies to products that have sizes.
    if size:
        if item_id in list(trolley.keys()):
            if size in trolley[item_id]['item_size'].keys():
                trolley[item_id]['item_size'][size] += quantity
            else:
                trolley[item_id]['item_size'][size] = quantity
        else:
            trolley[item_id] = {'item_size': {size: quantity}}
    else:

        # This block of code will update the quantity if the same item is
        # already in the trolley, if not then it will add the item to the
        # shopping trolley and overwrite the session variable with the
        # updated the session and then redirect using the redirect url
        if item_id in list(trolley.keys()):
            trolley[item_id] += quantity
        else:
            trolley[item_id] = quantity

    request.session['trolley'] = trolley
    return redirect(redirect_url)


def adjust_trolley(request, item_id):
    """
    Adjust the product quantity to the users specified
    amount within the shopping trolley
    """

    # Setting and initializing variables
    quantity = int(request.POST.get('product_quantity'))
    size = None
    # Checking if products have a size and creating trolley session
    if 'clothing_sizes' in request.POST:
        size = request.POST['clothing_sizes']
    trolley = request.session.get('trolley', {})

    # If the product has sizes and is greater than zero
    # then set the product quantity accordingly or update if already
    # in the shopping trolley or remove it from the shopping trolley
    # if quantity is below zero.
    if size:
        if quantity > 0:
            trolley[item_id]['item_size'][size] = quantity
        else:
            del trolley[item_id]['item_size'][size]
            if not trolley[item_id]['item_size']:
                trolley.pop(item_id)
    else:
        # Same as the above but only for quantity not sizes
        if quantity > 0:
            trolley[item_id] = quantity
        else:
            trolley.pop(item_id)

    request.session['trolley'] = trolley
    # Once the quantity is updated by the user and submitted
    # they will be taken back to the trolley page
    return redirect(reverse('view_trolley'))


def remove_from_trolley(request, item_id):
    """
    Remove an item from the shopping trolley
    """
    # try block used to catch server errors
    try:
        size = None
        # Checking if products have a size and creating trolley session
        if 'clothing_sizes' in request.POST:
            size = request.POST['clothing_sizes']
        trolley = request.session.get('trolley', {})

        # If the item has a size remove specific item user has specified
        # by removing the size key in the size dictionary and empty items
        if size:
            del trolley[item_id]['item_size'][size]
            if not trolley[item_id]['item_size']:
                trolley.pop(item_id)
        else:
            trolley.pop(item_id)

        request.session['trolley'] = trolley
        # returning a 200 response when item is removed because javascript
        # is being used
        return HttpResponse(status=200)

    # Returning a 500 server error
    except Exception as e:
        return HttpResponse(status=500)
