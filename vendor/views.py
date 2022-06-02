
from datetime import datetime, timedelta
from queue import Empty
from dateutil.relativedelta import relativedelta
import json
from django import urls
import simplejson
from random import random, randrange
from re import T, sub
from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from urllib3 import HTTPResponse
from order.models import Order
from decimal import Decimal
from product.models import Color, Product, Size, SubCategory
from .forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from vendor.models import Vendor
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from product.models import Category ,Image
from product.forms import ProductForm
from django.utils.text import slugify
import stripe
from django.contrib import messages
from djstripe.models import  Plan
from djstripe.models import Product as Product_p 
import djstripe
from django.views.decorators.csrf import csrf_exempt , requires_csrf_token
from django.core import serializers
from notifications.signals import notify
import jsonpickle
from json import JSONEncoder

acer = User.objects.get(username='acer')
# Create your views here.
def become_a_vendor(req):
    if req.method =='POST':
         form = UserCreationForm(req.POST) 
         if form.is_valid():
             user = form.save()
             login(req,user)
             vendor = Vendor.objects.create(
                 name=user.username,
                 created_by=user
             )
    else:
        form=UserCreationForm()
    
    return render(req,'vendor/become_a_vendor.html',{'form':form})

@login_required
def vendor_home(req):
    
    vendor = req.user.vendor
    products = Product.objects.filter(vendor=vendor)
    orders = vendor.orders.all()
    recent_orders= orders[0:4]
    li = []
    # for p in products : 
    #     serialized= serializers.serialize('json',[p,])
    #     loaded = json.loads(serialized)
    #     dumped = json.dumps(loaded[0])
    #     li.append(dumped)
    for p in products :
        product = {
            'id':p.id,
            'title':p.title,
            'slug':p.slug,
            'category_name':p.category.name,
            'category_slug':p.category.slug,
            'subcategory_name':p.Subcategory.name,
            'subcategory_slug':p.Subcategory.slug,
            'thumb':p.thumb.url,
            'price':str(p.price),
            'date':str(p.date),
        }
        li.append(product)
    #print(li)
    
    queryset = {
        'name':'',
        'list':li
    }    
    orders_data = []
    orders_labels = []
    EarningsData={
            'months':[],
            'amounts':[],
        }
    category_data={
        'category':[],
        'amounts':[],
    }
    today = datetime.today()
    
    def getOrdersBymonth(month):
        return Order.objects.filter(vendors__in=[vendor.id] ,created_at__month=month).count()
    def getOrderData():
        for i in range(1,7):
            month = today  - relativedelta(months=i)
            data= getOrdersBymonth(month.strftime('%m'))
            Month = datetime.strptime(month.strftime("%m"),"%m")
            orders_labels.append(Month.strftime('%b'))
            orders_data.append(data)
        orders_labels.reverse()   
        this_month = today.strftime("%m")
        This_Month = datetime.strptime(this_month,"%m")
        orders_data.append(getOrdersBymonth(this_month))
        orders_data.append('50')
        orders_labels.insert(7,This_Month.strftime("%b"))

    getOrderData()

    def getEarningsData():
        total_earnings = 0.00
        def getEarningsByMonth(month):
            items = vendor.items.filter(vendor_paid=True,order__vendors__in=[vendor.id])
            items= items.filter(created_at__month = month)
            data = sum(item.get_total_price() for item in items)
            return  str(data)
        for i in range(1,7):
            month = (datetime.today() - relativedelta(months=i)).strftime('%m')
            Month = datetime.strptime(month,"%m")
            EarningsData['months'].append(Month.strftime('%b'))
            EarningsData['amounts'].append(getEarningsByMonth(month))
            total_earnings += float(getEarningsByMonth(month) )
        this_month = datetime.today().strftime('%m')
        this_Month = datetime.strptime(this_month,"%m")
        EarningsData['months'].reverse()
        EarningsData['amounts'].reverse()
        EarningsData['months'].append(this_Month.strftime('%b'))
        EarningsData['amounts'].append(getEarningsByMonth(this_month))
        if total_earnings == 0 :
            EarningsData['amounts'].append(str(5000))
        print(EarningsData)
        print (total_earnings)
        #return json.dumps(EarningsData)
    getEarningsData()
    def getCategoriesData():
            items = vendor.items.filter(vendor_paid=True,order__vendors__in=[vendor.id])
            def categoryData(category):
                data = 0
                for item in items:
                    if item.product.category == category:
                            data += item.get_total_price()
                return str(data)
            for category in Category.objects.all():
                category_data['category'].append(category.name)
                category_data['amounts'].append(categoryData(category))
            print(category_data)
    getCategoriesData()       

    for order in orders:
        order.vendor_paid_amount =0
        order.vendor_amount = 0
        order.fully_paid = True
        
        for item in order.items.all():
            if item.vendor == req.user.vendor:
               if  item.vendor_paid:
                    order.vendor_paid_amount+= item.get_total_price()

                    

                    # for order in Orders.filter(created_at__month=4) :
                    #      April+=order.vendor_paid_amount
                    #      print( April )

               else:
                   order.vendor_amount += item.get_total_price()
                   orders.fully_paid = False
    context = {'vendor':vendor,'products':products,
                'orders':orders,'orders_data':json.dumps(orders_data),
                'orders_labels':json.dumps(orders_labels),'earnings_data':simplejson.dumps(EarningsData['amounts']),
                'category_data':json.dumps(category_data['amounts']),'category_list':json.dumps(category_data['category']),
                'recent_orders':recent_orders,'queryset':queryset}
    return render(req,'vendor/admin/vendor_home.html',context)

@login_required
def vendor_orders(req):
    
    if req.method == "POST":
        status = req.POST['status']
        order_id = req.POST['order_id']
        order = Order.objects.get(id=int(order_id))
        order.status = status
        order.save()
        return redirect('vendor_orders')
    vendor = req.user.vendor
    orders = vendor.orders.all()
    products=vendor.products.all()
    status=req.GET.get('status','')
    li =[]
    for p in products :
        product = {
            'id':p.id,
            'title':p.title,
            'slug':p.slug,
            'category_name':p.category.name,
            'category_slug':p.category.slug,
            'subcategory_name':p.Subcategory.name,
            'subcategory_slug':p.Subcategory.slug,
            'thumb':p.thumb.url,
            'price':str(p.price),
            'date':str(p.date),
        }
        li.append(product)
    queryset = {
        'name':'',
        'list':json.dumps(li)
    }
    if status:
        if status == 'delivered':
            orders = vendor.orders.filter(status="Delivered")
        elif status == 'pending':
            orders = vendor.orders.filter(status='Pending')
        elif status == 'dispatch':
            orders = vendor.orders.filter(status='Dispatch')
        
            
    


    for order in orders:
        order.vendor_paid_amount =0
        order.vendor_amount = 0
        order.fully_paid = True
        for item in order.items.all():
            if item.vendor == req.user.vendor:
               if  item.vendor_paid:
                    order.vendor_paid_amount+= item.get_total_price()
               else:
                   order.vendor_amount += item.get_total_price()
                   orders.fully_paid = False
             

    return render(req,'vendor/admin/dashboard_orders.html',{'vendor':vendor,'orders':orders,'status':status,'queryset':queryset,})

@login_required
def vendor_products(req):
    
    sizes = Size.objects.all()
    colors = Color.objects.all()
    sub_categories = serializers.serialize('json', SubCategory.objects.all())
    print(sub_categories)
    vendor = req.user.vendor
    #plan = Plan.objects.get(id=1)
    products = Product.objects.filter(vendor=vendor)
    li =[]
    for p in products :
        product = {
            'id':p.id,
            'title':p.title,
            'slug':p.slug,
            'category_name':p.category.name,
            'category_slug':p.category.slug,
            'subcategory_name':p.Subcategory.name,
            'subcategory_slug':p.Subcategory.slug,
            'thumb':p.thumb.url,
            'price':str(p.price),
            'date':str(p.date),
        }
        li.append(product)
    queryset = {
        'name':'products',
        'list':json.dumps(li)
    }
    remove_product = req.GET.get('remove_product','')
    if remove_product:
        product=Product.objects.get(id=remove_product)
        product.delete()
        messages.info(req,'The Product was deleted  successfuly !!')
        return redirect('vendor_products')

    if req.method == 'POST':
        form = ProductForm(req.POST,req.FILES)
        # if form.is_valid():
        #         product = form.save(commit=False)
        #         product.vendor = req.user.vendor
        #         product.slug = slugify(product.title)
        #         product.save()
        title = req.POST['title']
        thumb = req.FILES['thumb']
        desc = req.POST['desc']
        price = req.POST['price']
        quantity = req.POST['quantity']
        images = req.FILES.getlist('images')
        sizes = req.POST.getlist('sizes')
        colors = req.POST.getlist('colors')
        category = Category.objects.get(id=int(req.POST['category']))
        sub_category = SubCategory.objects.get(id=int(req.POST['sub_category']))  

        # product = Product.objects.create(title=title,thumb=thumb,desc=desc,price=price,category=category)
        product = Product()
        
        product.title=title
        product.thumb=thumb
        product.desc=desc
        product.price=price
        product.quantity=quantity
        product.category=category
        product.Subcategory=sub_category
        product.vendor = req.user.vendor
        product.slug = slugify(product.title,allow_unicode=True)
        product.save()
        notify.send(acer,recipient=req.user,verb='Your Product has been Created successfuly we have to be sure that it doesnt include anything can harm our policy! thanks for your patient :)  ',level='success')
        if sizes:
            for size in sizes:
                s= Size.objects.get(id=size)
                if s:
                    product.sizes.add(s)
        if colors:
            for color in colors:
                c= Color.objects.get(id=color)
                if c:
                    product.colors.add(c)
        
        if images:
                for image in images :
                        Image.objects.create(product=product,image=image)
        
        return redirect('vendor_products') 
    else:
            form = ProductForm()
    return render(req,'vendor/admin/dashboard_products.html',{'vendor':vendor,'products':products,'randomnumber':randrange(0,100),'sub_categories':sub_categories,'sizes':sizes,'colors':colors,'queryset':queryset})
@login_required

    
         
@login_required
def edit_vendor(req):
    vendor = req.user.vendor
    
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        profile_img = req.FILES['profile_img']
        if name:
            vendor.created_by.email = email
            vendor.created_by.save()
            
            vendor.name=name
            vendor.save()
            return redirect('vendor_admin')

    return render(req,'vendor/edit_vendor.html',{'vendor':vendor})
@login_required
def vendor_settings(req):
    vendor = req.user.vendor
    
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        profile_img = req.FILES['profile_img']
        if name:
            vendor.created_by.email = email
            vendor.created_by.save()
            vendor.profile = profile_img
            vendor.name=name
            vendor.save()
            return redirect('vendor_home')
    return render(req,'vendor/admin/dashboard_settings.html',{'vendor':vendor})
@login_required
def vendor_plans(req):
    stripe_public_key = settings.STRIPE_TEST_PUBLIC_KEY
    products= Product_p.objects.all()
    return render(req,'vendor/admin/dashboard_plans.html',{'products':products,'stripe_public_key':stripe_public_key})



def vendors(req):
    vendors = Vendor.objects.all()
    return render(req,'vendor/vendors.html',{'vendors':vendors})

def vendor(req,vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    return render(req,'vendor/vendor.html',{'vendor':vendor})




@csrf_exempt
def create_sub(request):
  vendor = request.user.vendor
  
  if request.method == 'POST':
      # Reads application/json and returns a response
      data = json.loads(request.body)
      payment_method = data['payment_method']
      stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

      payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
      djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


      try:
          # This creates a new Customer and attaches the PaymentMethod in one API call.
          customer = stripe.Customer.create(
              payment_method=payment_method,
              email=vendor.created_by.email,
              invoice_settings={
                  'default_payment_method': payment_method
              }
          )

          djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
          vendor.customer = djstripe_customer
         

          # At this point, associate the ID of the Customer object with your
          # own internal representation of a customer, if you have one.
          # print(customer)

          # Subscribe the user to the subscription created
          subscription = stripe.Subscription.create(
              customer=customer.id,
              items=[
                  {
                      "price": data["price_id"],
                  },
              ],
              expand=["latest_invoice.payment_intent"]
          )

          djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

          vendor.subscription = djstripe_subscription
          vendor.save()

          return JsonResponse(subscription)
      except Exception as e:
          return JsonResponse({'error': (e.args[0])}, status =403)
  else:
    return HTTPResponse('requet method not allowed')

def complete(req):
    return render(req,'vendor/admin/subscription_complete.html')