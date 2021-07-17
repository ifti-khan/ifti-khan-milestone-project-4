from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from trolley.contexts import trolley_contents

import stripe

def checkout(request):
    """
    Creating the checkout view which uses the shopping trolley session
    and if a session has not yet been created then a message will infrom
    the user that there shopping trolley is empty and redirect them back
    to the products page. Also creating an empty instance of the order form,
    creating the checkout template, adding the order form to the context
    processor and lastly rendering it all out.
    """
    # Setting the public and secret key vars for stripe from main settings
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    trolley = request.session.get('trolley', {})
    if not trolley:
        messages.error(request, "Your shopping trolley is empty,\
            please add a product to your shopping trolley")
        return redirect(reverse('products'))

    # Storing current shopping trolley in var called current_bag
    # Also getting the final total key from the current trolley and
    # setting the stripe total as integer
    current_bag = trolley_contents(request)
    total = current_bag['final_total']
    stripe_total = round(total * 100)

    # Setting the secrect key on stripe, creating the payment
    # intent and setting the stripe currency from main setting file
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Stripe message if dev forgets to add stripe public key to env
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Please set in your environment')

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        # Stripe public key
        'stripe_public_key': stripe_public_key,
        # Client secret key with intent
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
