from audioop import reverse
import random

from core.models import Banner
from .models import Image, Review, Size, SubCategory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from django.contrib import messages
from cart.cart import Cart
from .forms import AddToCartForm

from product.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from product.models import Category, Product
from django.db.models import Q
from notifications.signals import notify
 
acer = User.objects.get(username='acer')

def search(req):
        query = req.GET.get('query','')
        category = req.GET.get('category','')
        
        #products = Product.objects.filter(title=query)
        if query :
                products = Product.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query ))
                if category :
                       products =  products.filter(category__slug=category)
        return render(req,'product/search.html',{'products':products,'query':query})

def create_product(req):
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
        category = Category.objects.get(id=int(req.POST['category']))
        # product = Product.objects.create(title=title,thumb=thumb,desc=desc,price=price,category=category)
        product = Product()
        
        product.title=title
        product.thumb=thumb
        product.desc=desc
        product.price=price
        product.quantity=quantity
        product.category=category
        product.vendor = req.user.vendor
        product.slug = slugify(product.title)
        product.save()
        if images:
                for image in images :
                        Image.objects.create(product=product,image=image)
        
        return redirect('vendor_products') 
    else:
            form = ProductForm()

    return render(req,'product/create_product.html',{"form":form})

def edit_product(req,product_id):
    product = Product.objects.get(id=product_id)
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
        images = req.FILES.getlist('images')
        category = Category.objects.get(id=int(req.POST['category']))
        subcategory = SubCategory.objects.get(id=int(req.POST['sub_category']))
        sizes =  req.POST.getlist('sizes')
        colors =  req.POST.getlist('colors')

        # product = Product.objects.create(title=title,thumb=thumb,desc=desc,price=price,category=category)
        
        
        product.title=title
        product.thumb=thumb
        product.desc=desc
        product.price=price
        product.category=category
        product.vendor = req.user.vendor
        product.slug = slugify(product.title,allow_unicode=True)
        product.Subcatgory = subcategory
        product.save()
        notify.send(acer,recipient=req.user,verb='Your Product has been Updated successfuly !! ',level='success')
        if sizes:
                if product.sizes.all():
                        product.sizes.clear()
                for size in sizes:
                        product.sizes.add(size)
        if colors:
                if product.colors.all():
                        product.colors.clear()
                for color in colors:
                        product.colors.add(color)
        if images:
                if product.images:
                        for image in product.images.all() :
                                image.delete()
                for image in images :
                        Image.objects.create(product=product,image=image)
                        
        
        return redirect('vendor_products') 
    else:
            form = ProductForm()

    return render(req,'product/edit_product.html',{"form":form,'product':product})     
def product(req,category_slug,subcategory_slug,product_slug):
        cart = Cart(req)
        product = get_object_or_404(Product,category__slug=category_slug,Subcategory__slug=subcategory_slug,slug=product_slug)
        if product.status :
                
                review_text = req.GET.get('desc','')
                review_rate = req.GET.get('rate','')
                review = None
                try:
                         review=Review.objects.get(user=req.user,product=product)
                except Exception:
                        print('something is wrong')
                if review_rate and review_text :
                        if review:
                                review.rate = review_rate
                                review.text = review_text
                                review.save()
                        else:
                              Review.objects.create(user=req.user,product=product,rate=review_rate,text=review_text)  

                        return redirect('product' , category_slug= product.category.slug ,subcategory_slug= product.Subcategory.slug , product_slug= product.slug)
                if req.method == 'POST':
                        quantity = req.POST['quantity']
                        color = req.POST.get('color',False)
                        size = req.POST.get('size',False) 
                        cart.add(product_id=product.id ,quantity=quantity,update_quantity=False)
                        if color:
                                        cart.addColor(product_id=product.id,color=color)
                        if size :
                                cart.addSize(product_id=product.id,size=size)
                        if str(product.id) in cart.cart.keys() :
                                messages.success(req,'The Product was added successfully to the cart !')
                                return redirect('product' , category_slug= product.category.slug ,subcategory_slug= product.Subcategory.slug , product_slug= product.slug)
                        
                else:
                        form = AddToCartForm()
        else:
                if req.user == product.vendor.created_by  :
                        messages.warning(req ,'This Product hasn"t been active yet , please wait tl it be activated ')
                        return redirect('vendor_products')
                else:
                        return redirect('frontpage')

        semillar_products = list(product.category.products.exclude(id=product.id))
        #semillar_products = Product.objects.filter(category__slug=category_slug).exclude(id=product.id)
        if len(semillar_products) >=4:
                 semillar_products= random.sample(semillar_products,4)
        
        return render(req,'product/product.html',{'product':product,'semillar_products':semillar_products,'reviews':Review.objects.filter(product=product),'rev':review})

def category(req,category_slug):
    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(category__slug =category_slug,)
    product_id = req.GET.get('product_id','')
    favorites_id = req.GET.get('favorites_id','')
    favorites_remove_id =req.GET.get('favorites_remove_id','')
    cart =Cart(req)
    update_id = req.GET.get('change_quantity','')
    quantity = req.GET.get('quantity','')
    remove_id = req.GET.get('remove_from_cart','')

    if update_id != '':
        Cart(req).add(product_id=update_id,quantity=quantity,update_quantity=True)
    if remove_id != '':
        Cart(req).remove(remove_id)
    if product_id:
        cart.add(product_id=product_id)
        messages.success(req,'The Product was added successfully to the cart !')
    if favorites_id :
        product = Product.objects.get(id=favorites_id)
        product.favorites.add(req.user)
    if favorites_remove_id:
        product = Product.objects.get(id=favorites_remove_id)
        product.favorites.remove(req.user)
    return render(req,'product/category.html',{'category':category,'products':products})

def subcategory(req,category_slug,subcategory_slug):
    category = get_object_or_404(Category,slug=category_slug)
    subcategory = get_object_or_404(SubCategory,slug=subcategory_slug,category__slug=category_slug)
    products = Product.objects.filter(category=category,Subcategory=subcategory)
    product_id = req.GET.get('product_id','')
    favorites_id = req.GET.get('favorites_id','')
    favorites_remove_id =req.GET.get('favorites_remove_id','')
    cart =Cart(req)
    update_id = req.GET.get('change_quantity','')
    quantity = req.GET.get('quantity','')
    remove_id = req.GET.get('remove_from_cart','')

    if update_id != '':
        Cart(req).add(product_id=update_id,quantity=quantity,update_quantity=True)
    if remove_id != '':
        Cart(req).remove(remove_id)
    if product_id:
        cart.add(product_id=product_id)
        messages.success(req,'The Product was added successfully to the cart !')
    if favorites_id :
        product = Product.objects.get(id=favorites_id)
        product.favorites.add(req.user)
    if favorites_remove_id:
        product = Product.objects.get(id=favorites_remove_id)
        product.favorites.remove(req.user)
    return render(req,'product/category.html',{'subcategory':subcategory,'category':category,'products':products})