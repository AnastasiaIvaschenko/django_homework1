from django import template

register = template.Library()


# Это регистрация шаблонного ФИЛЬТРА
@register.filter
def mediapath(image_path):
    if image_path:
        return f'/media/{image_path}'
    return 'media/catalog/No_photo'


# Это регистрация шаблонного ТЕГА
@register.simple_tag
def mediapath(image_path):
    if image_path:
        return f'/media/{image_path}'
    return 'media/catalog/No_photo'
