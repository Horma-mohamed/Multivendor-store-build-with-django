from django import template
from django.conf import settings
from cart.context_processors import favourites
from cart.favorites import Favorites

register = template.Library()

@register.filter
def Isit(v):
    if v in settings.KEYS:
             return True
    else:
        return False
   