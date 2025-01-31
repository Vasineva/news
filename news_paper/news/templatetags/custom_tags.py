"""
Этот код определяет пользовательский шаблонный тег url_replace,
который позволяет изменять GET-параметры в URL.
"""
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()