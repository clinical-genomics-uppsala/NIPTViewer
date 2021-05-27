from django.template.defaulttags import register


@register.filter(name='min_value')
def min_value(value1, value2):
    return min(float(value1), float(value2))
