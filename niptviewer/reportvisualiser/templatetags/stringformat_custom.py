from django import template

register = template.Library()

@register.filter
def stringformat_custom(value, format):
    if value is None:
        return "NA"
    else:
        return ("{:" + format + "}").format(value)
