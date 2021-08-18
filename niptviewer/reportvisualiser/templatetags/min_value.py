from django.template.defaulttags import register


@register.filter(name='min_value')
def min_value(value1, value2):
    try:
        return min(float(value1), float(value2))
    except ValueError:
        if value1 == '':
            return value2
        else:
            return value1
