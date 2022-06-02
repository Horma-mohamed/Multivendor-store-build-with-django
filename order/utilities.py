from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



from cart.cart import Cart
from .models import *
from product.models import Product
from notifications.signals import notify



def checkout(req,user,first_name,last_name,email,phone,address,zipcode,place,amount):
    user = User.objects.get(username='acer')
    order = Order.objects.create(user=user,first_name=first_name,phone=phone,last_name=last_name,email=email,address=address,place=place, zipcode=zipcode,paid_amount=amount)
    for item in Cart(req):
        product = Product.objects.filter(pk=int(item['id']))[0]
        OrderItem.objects.create(order=order,product=product,vendor=product.vendor,price=product.price,quantity=item['quantity'],size='XL',color='Sky')
        notify.send(user,recipient=product.vendor.created_by,verb=' Someone bought your product  !!')
        order.vendors.add(product.vendor)   
    
    return order
    

def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for vendor in order.vendors.all():
        to_email = vendor.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


