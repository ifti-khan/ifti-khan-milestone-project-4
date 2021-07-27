from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # Changing the product admin columns
    # using the list display attribute
    list_display = (
        'sku',
        'product_name',
        'category',
        'product_price',
        'product_rating',
        'product_image',
    )

    # Sorting the product admin columns
    # using sku ascending
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    # Changing the categories admin columns
    # using the list display attribute
    list_display = (
        'category_friendly_name',
        'category_name',
    )


class ReviewAdmin(admin.ModelAdmin):
    # Changing the review admin columns
    # using the list display attribute
    list_display = (
        'product',
        'user',
        'review_title',
        'review_rating',
        'review_message',
        'date_created',
        'time_created',

    )

    # Sorting the review admin columns
    ordering = ('-date_created', '-time_created')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
