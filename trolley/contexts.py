from decimal import Decimal
from django.conf import settings


def trolley_contents(request):

    # creating empty list for trolley items and
    # initializing total and product count to zero
    trolley_items = []
    total = 0
    product_count = 0

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
