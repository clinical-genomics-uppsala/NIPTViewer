from django import template

register = template.Library()

@register.filter
def flag_sample(value):
    if value is None:
        return 'class=red'
    else:
        return ""
