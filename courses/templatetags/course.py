from django import template
from django.contrib.auth.models import Group

register = template.Library()


# Filter that return a generic content model name
@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.filter
# Check if a user belong to a specific group
def has_group(user, group_name):
    """
    {% if request.user|has_group:'grouName' %}
      {# do_stuff #}
    {% endif %}

    return Boolean (True/False)
    """
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()
