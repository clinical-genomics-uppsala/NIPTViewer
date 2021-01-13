from django.template.defaulttags import register


@register.simple_tag(name='model_lookup')
def model_lookup(value, arg):
    return getattr(value, arg)
