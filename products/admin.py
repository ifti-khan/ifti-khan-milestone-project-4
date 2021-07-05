from django.contrib import admin
from .models import Product, Category

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


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
