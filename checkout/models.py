# Used to generate the order number
import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

# Importing country fields for the stripe country dropdown
from django_countries.fields import CountryField

# Used in the line item model for the foreign keys
from products.models import Product

# Importing the users models
from profiles.models import UserProfile


class Order(models.Model):
    """
    This block of code is for the order model which will handle orders
    and contains generic character fields both required and not required
    like the postcode, county and country. Also the order number field will
    be auto generated, just like the date field when an order is created
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)

    # Creating the user profile foreign key, set null used so an order history
    # is kept if the user is deleted, this also allows users without an account
    # to make purchases. A related name has also been set so that it be used
    # to access users orders.
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders')

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email_address = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    address_line1 = models.CharField(max_length=80, null=False, blank=False)
    address_line2 = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    final_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)

    # two new fields which allows customers to purchase the same product
    # twice at different times.
    original_trolley = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        The code within this private method will generate a random,
        unique 32 character order number using UUID import at the top.
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        This code within the save method will, override the original
        save method to set the order number if on has not been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def update_total(self):
        """
        This code within the update total method, will update the final total
        each time a line item is added and taking into account for
        the delivery costs. It does this buy using the import sum located
        at the top.
        """
        # or 0 will prevent an error if the all line items are manually deleted
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_LIMIT:
            self.delivery_cost = self.order_total * \
                settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.final_total = self.order_total + self.delivery_cost
        self.save()

    # String method returning the order number
    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    This block of code is for the order line item model, which is
    related using foreign keys to the order model but this model
    deals with individual shopping trolley item that is linked
    to a specific order.
    """
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    # My product sizes XS, S, M, L, XL, XXL, XXXL
    product_size = models.CharField(
        max_length=4, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False,
        editable=False)

    def save(self, *args, **kwargs):
        """
        This code within the save method will, override the original save
        method to set the lineitem total and update the order total by
        multiplying the product price and quantity of each line item.
        """
        self.lineitem_total = self.product.product_price * self.quantity
        super().save(*args, **kwargs)

    # String method returning the product sku and order number
    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
