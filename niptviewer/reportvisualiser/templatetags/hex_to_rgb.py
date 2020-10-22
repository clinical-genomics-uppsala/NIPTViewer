from django.template.defaulttags import register

@register.simple_tag(name='hex_to_rgb')
def hex_to_rgb(value,opacity):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))+ (opacity,)
