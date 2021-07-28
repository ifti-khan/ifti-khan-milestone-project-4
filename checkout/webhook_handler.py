from django.http import HttpResponse

# Django imports to help with sending emails
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        # Getting customers email
        cust_email = order.email_address
        # Rendering confirmation_email_subject file to subject
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        # Rendering confirmation_email_body file to body
        # and contact email located in settings
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        # This sends using the send mail function and inside of it is the
        # subject, body, contact email and users email
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

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
                profile.default_full_name = shipping_details.name
                profile.default_email_address = billing_details.email
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
                    address_line1__iexact=shipping_details.address.line1,
                    address_line2__iexact=shipping_details.address.line2,
                    town_or_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
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
            # Sending confirmation email
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                # Creating the form to save within the webhook
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email_address=billing_details.email,
                    phone_number=shipping_details.phone,
                    address_line1=shipping_details.address.line1,
                    address_line2=shipping_details.address.line2,
                    town_or_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    user_profile=profile,
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
                        for size, quantity in item_data['item_size'].items():
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
        # Sending confirmation email using the webhook
        self._send_confirmation_email(order)
        # The order has been created by the webhook 200 http response
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
