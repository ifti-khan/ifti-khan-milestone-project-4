from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """
    Creating the checkout view which uses the shopping trolley session
    and if a session has not yet been created then a message will infrom
    the user that there shopping trolley is empty and redirect them back
    to the products page. Also creating an empty instance of the order form,
    creating the checkout template, adding the order form to the context
    processor and lastly rendering it all out.
    """
    trolley = request.session.get('trolley', {})
    if not trolley:
        messages.error(request, "Your shopping trolley is empty,\
            please add a product to your shopping trolley")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)