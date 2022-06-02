from email.policy import default
from django import forms
from .models import *
from cloudinary.models import CloudinaryField
class ProductForm(forms.ModelForm):
    #thumb =forms.ImageField(required=False, upload_to='products/thumbs')
    class Meta:
        model = Product
        fields = ['title','thumb','desc','price','category']


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1 )