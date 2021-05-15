"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path,include
from django.views.generic import TemplateView

#from products.views import (
        #ProductListView,
        #product_list_view , 
        #ProductDetailView,
        #product_detail_view , 
        #ProductFeaturedDetailView ,
        #ProductFeaturedListView, 
        #ProductDetailSlugView
        #)
from accounts.views import login_page,register_page,guest_register_view
from .views import home_page,contact_page,about_page
from addresses.views import checkout_address_create_view,checkout_address_reuse_view

urlpatterns = [


    path('goel_enterprises/', home_page, name='home'),
    path('goel_enterprises/contact/',contact_page,name='contact'),
    path('goel_enterprises/register/',register_page,name='register'),
    path('goel_enterprises/bootstrap/',TemplateView.as_view(template_name="bootstrap/example.html")),
    path('goel_enterprises/login/',login_page,name='login'),
    path('goel_enterprises/logout/',LogoutView.as_view(),name='logout'),
    path('goel_enterprises/register/guest/',guest_register_view,name='guest_register'),
    path('goel_enterprises/about/',about_page,name='about'),
    path('goel_enterprises/checkout/address/create/',checkout_address_create_view,name='checkout_address_create'),
    path('goel_enterprises/checkout/address/reuse/',checkout_address_reuse_view,name='checkout_address_reuse'),
    path('goel_enterprises/cart/',include(('carts.urls','carts'), namespace='cart')),
    path('goel_enterprises/products/',include(('products.urls','products'), namespace='products')),
    path('goel_enterprises/search/',include(('search.urls','search'), namespace='search')),

    #path('products/',ProductListView.as_view()),
    #path('products-fbv/',product_list_view),
    #path('products/<int:pk>/',ProductDetailView.as_view()),
    #path("products-fbv/<int:pk>/",product_detail_view),
    #path("featured/",ProductFeaturedListView.as_view()),
    #path("featured/<int:pk>/",ProductFeaturedDetailView.as_view()),
    #path("products/<slug:slug>/",ProductDetailSlugView.as_view()),
    path('goel_enterprises/admin/', admin.site.urls),
]

#app_name = 'products'

if settings.DEBUG: 
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
