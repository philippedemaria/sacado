from django import template

register = template.Library()


@register.filter
def array_2d(List, i):
    return List[int(i)]
 