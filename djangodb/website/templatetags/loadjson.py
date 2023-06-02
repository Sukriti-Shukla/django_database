from django import template
import json

register = template.Library()

@register.filter(name='loadjson')
def loadjson(value):
    return json.loads(value)
