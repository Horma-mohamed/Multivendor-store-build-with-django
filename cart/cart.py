from itertools import product
from turtle import title
from django.conf import settings

from product.models import Product
from django.core import serializers

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def __iter__(self):
        pass
        for p in self.cart.keys():
            product = Product.objects.get(pk=p)
            self.cart[str(p)] = {'quantity':1, 'id': product.id, 'product': { 'title':product.title , 'product_slug':product.slug,'category':{'name':product.category.name,'slug':product.category.slug}, 'price':product.price, 'thumb':product.thumb.url  }}            
        for item in self.cart.values():
            item['total_price'] = product.price * item['quantity']

            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, product_id, quantity=1,update_quantity=False):
        product = Product.objects.get(pk=product_id)
        product_id = str(product_id)
        
        def total_price():
            return product.price * int(quantity) 
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': int(quantity), 'id': product_id, 'total_price':total_price() ,'product': { 'title':product.title , 'slug':product.slug,'category':{'name':product.category.name,'slug':product.category.slug},'subcategory':{'name':product.Subcategory.name,'slug':product.Subcategory.slug}, 'price':product.price, 'thumb':product.thumb.url  }}
            
        elif update_quantity==False :
            self.cart[product_id]['quantity'] = int(quantity)
            self.cart[product_id]['total_price'] = total_price()

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            self.cart[product_id]['total_price'] = product.price * self.cart[product_id]['quantity']

            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product_id)
                        
        self.save()
    def addColor(self,product_id,color='nothing'):
        product_id = str(product_id)
        self.cart[product_id]['product']['color'] = color
        self.save()
    def addSize(self,product_id,size):
        product_id = str(product_id)
        self.cart[product_id]['product']['size'] = size
        self.save()
    
    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        total_cost=0
        for item in self.cart.values():
            total_cost += item['total_price']
        return total_cost 
    