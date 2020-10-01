from django import template

register = template.Library()

@register.filter
def percentformat(value, decimals=0):
    return ("{:." + str(decimals) + "%}").format(value)
