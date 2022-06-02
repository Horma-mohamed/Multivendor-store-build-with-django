import imp
from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=255)
    theme = RichTextField()
    link = models.URLField(max_length=200,blank=True,null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField()