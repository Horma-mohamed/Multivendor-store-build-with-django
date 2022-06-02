import imp
from django import template
from django.conf import settings
from cart.context_processors import favourites
from cart.favorites import Favorites
from django.http import HttpRequest
from django.contrib.sessions.backends.db import SessionStore
from django.utils.html import html_safe , mark_safe

register = template.Library()

@register.simple_tag
def favorite(f,s):
    if str(f) in s :
        return mark_safe(f'<a href="?favorites_remove_id={f}" > <svg class="absolute right-4 top-3"  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="none" d="M0 0H24V24H0z"/><path d="M12.001 4.529c2.349-2.109 5.979-2.039 8.242.228 2.262 2.268 2.34 5.88.236 8.236l-8.48 8.492-8.478-8.492c-2.104-2.356-2.025-5.974.236-8.236 2.265-2.264 5.888-2.34 8.244-.228z" fill="rgba(249,86,70,1)"/></svg></a>')
    else:
        return mark_safe(f'<a href="?favorites_id={f}"  > <svg class="absolute right-4 top-3 fill-gray-300 "  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="none" d="M0 0H24V24H0z"/><path d="M12.001 4.529c2.349-2.109 5.979-2.039 8.242.228 2.262 2.268 2.34 5.88.236 8.236l-8.48 8.492-8.478-8.492c-2.104-2.356-2.025-5.974.236-8.236 2.265-2.264 5.888-2.34 8.244-.228z" fill="rgba(229,229,229,0.78)"/></svg></a>')


    
   