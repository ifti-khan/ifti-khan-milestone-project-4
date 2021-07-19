from django.contrib import admin

# Importing Order and OrderLineItems models
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    This inline item is going to allow the admin to add and edit
    line items in the admin right from inside the order model.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Creating the order admin with read only field, so they cannot
    be editted by anyone. Also specifying the orders of the fields
    in the admin interface side of the project and restricting the
    columns that show up in the order list to a dew items.
    """

    # Adding the inline option to the order admin class
    inlines = (OrderLineItemAdminInline,)

    # Un-editable fields
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'final_total', 'original_trolley',
                       'stripe_pid')

    # Field order in the admin interface
    fields = ('order_number', 'date', 'full_name',
              'email_address', 'phone_number', 'address_line1',
              'address_line2', 'postcode', 'town_or_city',
              'county', 'country', 'order_total', 'delivery_cost',
              'final_total', 'original_trolley', 'stripe_pid')

    # To restrict order list columns to only show a few key items
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'final_total', 'original_trolley',
                    'stripe_pid')

    # Orders will be ordered by the most recent date being at the top
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
