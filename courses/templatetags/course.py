from django import template

register = template.Library()


# Filter that return a generic content model name
@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
