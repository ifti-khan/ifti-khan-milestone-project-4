from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def trolley_contents(request):

    # creating empty list for trolley items and
    # initializing total and product count to zero
    trolley_items = []
    total = 0
    product_count = 0
    # Getting trolley session if one exist, if not it will
    # create an empty dictionary
    trolley = request.session.get('trolley', {})

    # Iterating through all items in the shopping trolley and checking
    # if the item has a size, if no sizes then it will add
    # up the total cost, quantity and add the product data to the
    # trolley item list to be shown in the shopping trolley page template.
    # if it does then it will execute the code block after the else statement
    for item_id, item_data in trolley.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.product_price
            product_count += item_data
            trolley_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            # Iterating thorugh the dictionary item_size, then incrementing the
            # quantity and total accordingly and adding product size to render
            # to the trolley page template.
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['item_size'].items():
                total += quantity * product.product_price
                product_count += quantity
                trolley_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    # This block of code is calculates the free delivery limit on orders
    # which is £50 or more and if its not then will charge customers a delivery
    # fee of 10 percent of the total order.
    if total < settings.FREE_DELIVERY_LIMIT:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery = settings.FREE_DELIVERY_LIMIT - total
    else:
        delivery = 0
        free_delivery = 0

    final_total = delivery + total

    # context dictionary with keys and values to be
    # used in the rendered html template
    context = {
        'trolley_items': trolley_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery': free_delivery,
        'free_delivery_limit': settings.FREE_DELIVERY_LIMIT,
        'final_total': final_total,
    }

    return context
