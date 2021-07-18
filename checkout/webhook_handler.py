from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle Stripe webhooks and creates and instance once called.
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event from stripe
        and returns a HTTP response indicating a webhook has been recivied.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
