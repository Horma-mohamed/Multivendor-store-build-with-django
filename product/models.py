from cloudinary.models import CloudinaryField
from django.db import models
from vendor.models import Vendor
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering =['ordering']
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category,related_name='sub_categories',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering =['ordering']
    def __str__(self):
        return self.name

class Album(models.Model):
    thumb = CloudinaryField()
    def __str__(self):
        return f"album-{self.product.title}"
class Image(models.Model):
    image = CloudinaryField()
    #album= models.ForeignKey('product.album',related_name='images',on_delete=models.CASCADE)
    product= models.ForeignKey('product.product',related_name='images',on_delete=models.CASCADE)


class Review(models.Model):
    # rate = models.DecimalField(max_digits=1,default=0.5,decimal_places=1)
    rate = models.IntegerField(default=1)
    text = RichTextField()
    user = models.ForeignKey(User,related_name='reviews' , on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product',related_name='reviews',on_delete=models.CASCADE)


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    desc = RichTextField()
    slug = models.SlugField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    thumb = CloudinaryField()
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    Subcategory = models.ForeignKey(SubCategory,related_name='products',on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,related_name='products',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    album = models.OneToOneField(Album,related_name='product',on_delete=models.CASCADE,null=True,blank=True)
    favorites = models.ManyToManyField(User,related_name='favorites', blank=True,null=True)
    sizes = models.ManyToManyField("product.Size", related_name='products', null=True,blank=True)
    colors = models.ManyToManyField("product.Color", related_name='products' , null=True,blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Color(models.Model):
    name = models.CharField(max_length=60,unique=True)
    code = models.CharField(max_length=150,unique=True)
    def __str__(self) :
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=60,unique=True)
    #code = models.CharField(max_length=150,unique=True)
    def __str__(self) :
        return self.name

