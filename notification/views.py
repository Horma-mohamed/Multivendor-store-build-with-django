from django.shortcuts import render

# Create your views here.

def notiication(req):
    return render(req,'notification/notification.html',)