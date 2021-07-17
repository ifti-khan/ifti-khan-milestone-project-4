from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
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

    # Checking to see if the method is post and get the
    # shopping bag session. Also putting the order form data
    # into a dictionary.
    if request.method == 'POST':
        trolley = request.session.get('trolley', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email_address': request.POST['email_address'],
            'phone_number': request.POST['phone_number'],
            'address_line1': request.POST['street_address1'],
            'address_line2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        # If the order form is valid then it will be saved
        if order_form.is_valid():
            order = order_form.save()

            # This code was taken from my trolley context.py and modified
            for item_id, item_data in trolley.items():
                try:
                    # Getting product id out of the bag, if value is an
                    # integer, then product has no sizes and save the
                    # order line item.
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # Code taken from my trolley context.py and modified
                        # This is for orders which have sizes and iterates
                        # through each line item and saves them.
                        for size, quantity in item_data['item_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                clothing_sizes=size,
                            )
                            order_line_item.save()
                # Error message for product if not found in database, the order
                # is deleted and user is taken back to the view trolley page
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your shopping bag, \
                            could not be found in the database, \
                                Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_trolley'))
            # This session is for users who want to save there delivery
            # info to there personal profile and if all is successful then
            # the user will be taken to the checkout success page.
            request.session['save_del_info'] = 'save-del-info' in request.POST
            return redirect(
                reverse('checkout_complete', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your order form. \
                Please check the information you have entered.')
    else:
        trolley = request.session.get('trolley', {})
        if not trolley:
            messages.error(request, "Your shopping trolley is empty,\
            please add a product to your shopping trolley")
            return redirect(reverse('products'))

        # Storing current shopping trolley in var called current_bag
        # Also getting the final total key from the current trolley and
        # setting the stripe total as integer
        current_trolley = trolley_contents(request)
        total = current_trolley['final_total']
        stripe_total = round(total * 100)

        # Setting the secrect key on stripe, creating the payment
        # intent and setting the stripe currency from main setting file
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    # Stripe message if dev forgets to add stripe public key to env
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Please set in your environment')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        # Stripe public key
        'stripe_public_key': stripe_public_key,
        # Client secret key with intent
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_complete(request, order_number):
    """
    This view is for the checkout success letting the user know
    that the payment was successful and order has been completed
    """

    # Getting the delivery info session for the profile page,
    # also getting the previous orders order number to include
    # in the toast message to the user along with additional info
    save_del_info = request.session.get('save_del_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully completed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email_address}.')

    # Deleting users shopping trolley session
    if 'trolley' in request.session:
        del request.session['trolley']

    # Setting the template and context to be rendered
    template = 'checkout/checkout_complete.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
