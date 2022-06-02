from django.urls import path
from .views import *
urlpatterns = [
    
    path('',cart_details,name='cart'),
    path('success/',success,name='success')
]
