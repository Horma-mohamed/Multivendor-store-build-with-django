from django.shortcuts import render,redirect
from product.models import Product
import stripe 
from django.conf import settings
from django.contrib import messages
from .cart import Cart
from order.utilities import checkout
from .forms import CheckoutForm

# Create your views here.

def cart_details(req):
    update_id = req.GET.get('change_quantity','')
    quantity = req.GET.get('quantity','')
    remove_id = req.GET.get('remove_from_cart','')

    if update_id != '':
        Cart(req).add(product_id=update_id,quantity=quantity,update_quantity=True)
    if remove_id != '':
        Cart(req).remove(remove_id)

    if req.method == "POST":
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        email = req.POST['email']
        phone = req.POST['phone']
        address = req.POST['address']
        zipcode = req.POST['zipcode']
        place = req.POST['place']
        stripe_token =req.POST['stripe_token']
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            charge = stripe.Charge.create(
                amount = int(Cart(req).get_total_cost()*100),
                currency='usd',
                description='Charge from Multivendor Project ',
                source = stripe_token,
            )
        except Exception:
            return messages.error(req,' Somthing is Wrong with the payment !!! ')
        order= checkout(req,user=req.user,first_name=first_name,last_name=last_name,address=address,email=email,phone=phone,place=place,zipcode=zipcode,amount=5000)
        Cart(req).clear()
        return redirect('success')
    total_cost= Cart(req).get_total_cost()
    context = {'total_cost':total_cost,'stripe_pub_key':settings.STRIPE_TEST_PUBLIC_KEY}
    return render(req,'cart/cart_details.html',context)

def success(req):
    return render(req, 'cart/success.html')



"""
def cart_details(req):
    cart = Cart(req)
    for item in cart :
        print(item)
    if req.method == 'POST':
        form = CheckoutForm(req.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
            stripe_token = form.cleaned_data['stripe_token']
            try:
                charge = stripe.Charge.create(
                amount = int(cart.get_total_cost()*100),
                currency='USD',
                description='Charge from Multivendor Project ',
                source = stripe_token,
                )
            except Exception:
                return messages.error(req,'there was something wrong with payment !!')
            first_name = req.POST['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']
            order= checkout(req,user=req.user,first_name=first_name,last_name=last_name,address=address,email=email,phone=phone,place=place,zipcode=zipcode,amount=5000)
            cart.clear()
            return redirect('success')
                 
            
               
    else:
        form = CheckoutForm()
    

        update_id = req.GET.get('change_quantity','')
        quantity = req.GET.get('quantity','')
        remove_id = req.GET.get('remove_from_cart','')

        if update_id != '':
            Cart(req).add(product_id=update_id,quantity=quantity,update_quantity=True)
        if remove_id != '':
            Cart(req).remove(remove_id)

        total_cost = Cart(req).get_total_cost()
    return render(req , 'cart/cart_details.html',{'total_cost':total_cost,'form':form,'stripe_pub_key':settings.STRIPE_TEST_PUBLIC_KEY})



"""