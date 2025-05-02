from django import template

register = template.Library()

@register.filter
def sum_prices(cart):
    return sum(item['price'] for item in cart)
