from . import views
from django.urls import path

urlpatterns = [
    path('notification/',views.notiication,name='notification')
]
