from django.db import models
from product.models import Product
from vendor.models import Vendor
from django.contrib.auth.models import User
# Create your models here.

class Order(models.Model):
    STATUS_TYPES = (
        ('Pending','pending'),
        ('Delivered','delivered'),
        ('Dispatch','dispatch'),
        )
    user = models.ForeignKey(User,related_name='orders',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,choices=STATUS_TYPES,default="Pending")
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vendors = models.ManyToManyField(Vendor, related_name='orders')
    
    def get_cost(self):
        return sum( item.get_total_price() for item in self.items.all())
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.first_name

    # def total_price(self):
    #     total = 0
    #     for item in self.items:
    #         total+=item.get_total_price
    #     return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size= models.CharField(max_length=100, null=True,blank=True)
    color= models.CharField(max_length=100, null=True,blank=True)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return '%s' % self.id
    
    def get_total_price(self):
        return self.price * self.quantity


# class Earning(models):
#     month = models.DateField()