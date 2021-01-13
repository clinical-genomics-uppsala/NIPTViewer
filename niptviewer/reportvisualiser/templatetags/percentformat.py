from django import template

register = template.Library()


@register.filter
def percentformat(value, decimals=0):
    if value is None:
        return "NA"
    else:
        return ("{:." + str(decimals) + "%}").format(value)
