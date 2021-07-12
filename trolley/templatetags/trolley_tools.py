from django import template

register = template.Library()

# Custom template tag for subtotal calculation to be used
# within the trolley.html


@register.filter(name='calc_subtotal')
def calc_subtotal(product_price, quantity):
    return product_price * quantity
