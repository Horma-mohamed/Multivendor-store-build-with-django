from django.urls import path


from .views import *
from django.contrib.auth import views as auth_vw


urlpatterns = [
    path('become_a_vendor',become_a_vendor,name='become_a_vendor'),
    path('logout',auth_vw.LogoutView.as_view(),name='logout'),
    path('login',auth_vw.LoginView.as_view(template_name='vendor/login.html'),name='login'),    
    path('vendor/dashboard/',vendor_home,name='vendor_home'),
    path('vendor/dashboard/orders',vendor_orders,name='vendor_orders'),
    path('vendor/dashboard/products',vendor_products,name='vendor_products'),
    path('vendor/dashboard/settings',vendor_settings,name='vendor_settings'),
    path('vendor/dashboard/plans',vendor_plans,name='vendor_plans'),
    path('edit_vendor',edit_vendor,name='edit_vendor'),
    path('vendors',vendors,name='vendors'),
    path('vendors/<int:vendor_id>',vendor,name='vendor'),
    path("vendor/plans/create-sub", create_sub, name="create_sub"),
      path("complete", complete, name="complete"), 


]
 