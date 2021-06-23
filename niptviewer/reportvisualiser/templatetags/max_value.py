from django.template.defaulttags import register


@register.filter(name='max_value')
def max_value(value1, value2):
    try:
        return max(float(value1), float(value2))
    except:
        if value1 == '':
            return value2
        else:
            return value1
