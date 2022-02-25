from django import template

register = template.Library()


@register.simple_tag
def flag_sample(value1, field1=None, value2=None, field2=None):
    if value1 is None and value2 is None:
        return 'class=red'
    if field1 == "ff_formatted":
        if float(value1) < 0.02:
            return 'class=red'
    if field2 == "ff_formatted":
        if float(value2) < 0.02:
            return 'class=red'
    if field1 in ['ncv_13', 'ncv_18', 'ncv_21']:
        if 3 < float(value1) < 4:
            return 'class=orange'
        elif float(value1) > 4:
            return 'class=red'
    if field2 in ['ncv_13', 'ncv_18', 'ncv_21']:
        if 3 < float(value2) < 4:
            return 'class=orange'
        elif float(value2) > 4:
            return 'class=red'
    return ""
