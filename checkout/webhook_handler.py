from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time

# This code was learnt and added from the stripe video section,
# within the django mini project, specifcally video 10 and 11.


class StripeWH_Handler:
    """
    Handles Stripe webhooks.
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handles the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        # Getting and storing the payment intent id,
        # shopping trolley and save delivery info meta data
        pid = intent.id
        trolley = intent.metadata.trolley
        save_del_info = intent.metadata.save_del_info

        # Getting and storing the billing, shipping details
        # and the final total
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        final_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details and setting empty
        # strings as none instead of null
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_del_info was checked also
        # setting user to none so that non logged in users can make a
        # purchase,
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_del_info:
                profile.default_full_name = shipping_details.name,
                profile.default_email_address = shipping_details.email,
                profile.default_phone_number = shipping_details.phone
                profile.default_address_line1 = shipping_details.address.line1
                profile.default_address_line2 = shipping_details.address.line2
                profile.default_town_or_city = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_country = shipping_details.address.country
                profile.save()

        # Setting the order exist to false and then using the payment intent
        # to get the order info and then using iexact to make it an exact
        # match but case-insensitive
        order_exists = False
        # Creating a delay and setting the attempt to 1 and then a while
        # loop will execute up to 5 times
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email_address__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    final_total=final_total,
                    # adding on the shopping trolley and pid
                    original_trolley=trolley,
                    stripe_pid=pid,
                )
                # if the order does exist a 200 http response is sent to stripe
                # with a message that the order is verified and already exists
                order_exists = True
                break
            # If the order does not exist, it then needs to be created, just
            # like in the views.py
            except Order.DoesNotExist:
                # Incrementing the attempt by one and then using the python
                # sleep module to then make it sleep for one second
                attempt += 1
                time.sleep(1)
        # This is outside the while loop and will check to see if
        # order exists is true and if so return a 200 response
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                # Creating the form to save within the webhook
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email_address=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    address_line1=shipping_details.address.line1,
                    saddress_line2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    # adding on the shopping trolley and pid
                    original_trolley=trolley,
                    stripe_pid=pid,
                )
                # Code was taken from the checkouts views.py but the
                # shopping trolley is loaded from the json payment intent
                # instead of the trolley session
                for item_id, item_data in json.loads(trolley).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            # If anything goes wrong this deletes the order if it was created
            # and returns a 500 server error to stripe
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # The order has been created by the webhook 200 http response
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
