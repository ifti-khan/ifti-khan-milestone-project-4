from django.db import models


class Category(models.Model):

    # Adding a meta class specifying a verbose name of categories
    # instead of Django default category name on the admin page
    class Meta:
        verbose_name_plural = 'Categories'

    # Setting the programmatic name
    category_name = models.CharField(max_length=254)
    # Setting the friendly name
    category_friendly_name = models.CharField(
        max_length=254, null=True, blank=True)

    # Creating a string method for
    # the category name
    def __str__(self):
        return self.category_name

    # Creating a model method to
    # to return the friendly name
    def get_friendly_name(self):
        return self.category_friendly_name


class Product(models.Model):
    """
    Below you will find the product model which contains
    the key fields to store product information.
    Null and Blank true have been used throughout the model
    fields to make them optional.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=254)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    product_rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    sku = models.CharField(
        max_length=254, null=True, blank=True)
    product_sizes = models.BooleanField(default=False, null=True, blank=True)
    product_image = models.ImageField(null=True, blank=True,
                                      default='noimage_img.jpg')
    product_image_url = models.URLField(
        max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.product_name
