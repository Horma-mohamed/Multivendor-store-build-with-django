import imp


from django.urls import path
from .views import *
urlpatterns = [
    path('create_product',create_product,name='create_product'),
    path('edit_product/<int:product_id>',edit_product,name='edit_product'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<product_slug>',product,name='product'),
    path('<slug:category_slug>',category,name='category'),
    path('<slug:category_slug>/<slug:subcategory_slug>',subcategory,name='subcategory'),
    path('search/',search,name='search')
    
]
