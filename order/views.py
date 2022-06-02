import imp
from django.http import JsonResponse
from django.shortcuts import render

from .models import Order
from django.core import serializers
import datetime
from dateutil import parser
# Create your views here.

def orders_data(req):
    #datetime.datetime.fromisoformat()

    orders = Order.objects.all()
    dataset = [  ]
    dataset.append({
        'data':[
                orders.filter(created_at__month=1).__len__(),
                
                orders.filter(created_at__month=2).__len__()
                ,

                orders.filter(created_at__month=3).__len__()
                ,

                orders.filter(created_at__month=4).__len__()
                ,
                
                orders.filter(created_at__month=5).__len__()
                ,
                
                orders.filter(created_at__month=6).__len__()
                ,
                
                    orders.filter(created_at__month=7).__len__()
               ,]
            })
    return JsonResponse(dataset,safe=False)
