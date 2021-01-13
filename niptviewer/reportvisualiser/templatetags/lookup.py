from django.template.defaulttags import register


@register.simple_tag(name='lookup')
def lookup(value, arg):
    return value.get(arg)
