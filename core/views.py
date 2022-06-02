from atexit import register
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from cart.cart import Cart
from core.models import Banner
from product.models import Product
from cart.favorites import Favorites

from django import template
from django.template.defaultfilters import stringfilter

from djstripe.models import Product as Plan

# Create your views here.

    
def frontpage(req):
    #Favourites(req).clear()
    newest_products = Product.objects.all()[0:8]
    product_id = req.GET.get('product_id','')
    favorites_id = req.GET.get('favorites_id','')
    favorites_remove_id =req.GET.get('favorites_remove_id','')
    cart =Cart(req)
    banners = Banner.objects.all()
    update_id = req.GET.get('change_quantity','')
    quantity = req.GET.get('quantity','')
    remove_id = req.GET.get('remove_from_cart','')

    if update_id != '':
        Cart(req).add(product_id=update_id,quantity=quantity,update_quantity=True)
        return  redirect('frontpage')
    if remove_id != '':
        Cart(req).remove(remove_id)
        return  redirect('frontpage')
    if product_id:
        cart.add(product_id=product_id)
        messages.success(req,'The Product was added successfully to the cart !')
        return  redirect('frontpage')
   
        
    if favorites_id :
        product = Product.objects.get(id=favorites_id)
        product.favorites.add(req.user)
        return  redirect('frontpage')

    if favorites_remove_id:
        product = Product.objects.get(id=favorites_remove_id)
        product.favorites.remove(req.user)
        return  redirect('frontpage')


    return render(req,'core/frontPage.html',{'newest_products':newest_products,'banners':banners})


def pricing_page(req):
    plans = Plan.objects.all()
    return render(req,'core/pricing.html',{'products':plans})