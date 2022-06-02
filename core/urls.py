from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage,name='frontpage'),
    path('pricing',views.pricing_page,name='pricing_page')
]
