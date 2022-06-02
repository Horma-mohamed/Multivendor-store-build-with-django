from datetime import datetime
import json
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from dateutil.relativedelta import relativedelta
# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User,related_name='vendor',on_delete=models.CASCADE)
    profile = CloudinaryField()
    customer = models.ForeignKey('djstripe.Customer',null=True,blank=True,on_delete=models.SET_NULL)
    subscription = models.ForeignKey("djstripe.Subscription",related_name='vendor',null=True,blank=True, on_delete=models.SET_NULL)
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    def subscription_limite_near_reach(self):
        if self.subscription.plan.metadata['products_limite'] - self.products.all().count() ==1 :
            return True
        else:
            return False
    def get_balance(self):
        items = self.items.filter(vendor_paid=False,order__vendors__in=[self.id])
        return sum(item.product.price * item.quantity for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True,order__vendors__in=[self.id])
        return sum(item.product.price * item.quantity for item in items)
    def getEarningsData(self):
        EarningsData={
            'months':[],
            'amounts':[],
        }
        def getEarningsByMonth(month):
            items = self.items.filter(vendor_paid=True,order__vendors__in=[self.id])
            items= items.filter(created_at__month = month)
            data = sum(item.product.price * item.quantity for item in items)
            return  data
        for i in range(1,7):
            month = (datetime.today() - relativedelta(months=i)).strftime('%m')
            Month = datetime.strptime(month,"%m")
            EarningsData['months'].append(Month)
            EarningsData['amounts'].append(getEarningsByMonth(month))
        print(EarningsData)
        return json.dumps(EarningsData)
        
        