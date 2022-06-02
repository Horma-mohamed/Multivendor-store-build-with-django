from django.urls import path 
from .views import *
urlpatterns = [
    path('orders_data/',orders_data,name='orders_data')
]
