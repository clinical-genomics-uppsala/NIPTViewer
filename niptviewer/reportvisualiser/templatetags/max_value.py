from django.template.defaulttags import register


@register.filter(name='max_value')
def max_value(value1, value2):
    return max(float(value1), float(value2))
