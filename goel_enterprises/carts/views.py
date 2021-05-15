from django.shortcuts import render,redirect

from orders.models import Order
from products.models import Product
from .models import Cart
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


from addresses.forms import AddressForm

from addresses.models import Address
# Create your views here.

#def cart_create(user=None):
 #   cart_obj = Cart.objects.create(user=None)
  #  print("New cart created")
  #return cart_obj

def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    #products = cart_obj.products.all()
    #total =0
    #for x in products:
     #   total +=x.price
     #   print(total)
    #cart_obj.total = total
    #cart_obj.save()

    #del request.session['cart_id']
    #cart_id = request.session.get("cart_id",None)
    #if cart_id is None:      # and isinstance(cart_id,int):
        #cart_obj = cart_create()
        #request.session['cart_id'] = cart_obj.id
    #else:
    #qs = Cart.objects.filter(id=cart_id)
    #if qs.count()==1:
      #  print('Cart id exists')
       # cart_obj = qs.first()
        #if request.user.is_authenticated and cart_obj.user is None:
         #   cart_obj.user = request.user
          #  cart_obj.save()
    #else:
       # cart_obj =  Cart.objects.new(user=request.user)
        #request.session['cart_id'] = cart_obj.id
        #print(cart_id)
        #cart_obj = Cart.objects.get(id=cart_id)
    #print(request.session)
    #print(dir(request.session))
    # request.session.set_expiry(300) # 5 minutes
    #key = request.session.session_key
    #print(key)
    #request.session['cart_id'] = 12
    return render(request,"carts/home.html",{"cart":cart_obj})


def cart_update(request):
    #print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, Product is gone ?")
            return redirect("cart:home")
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
             cart_obj.products.remove(product_obj)
        else:
             cart_obj.products.add(product_obj)  #or  cart_obj.products.add(product_id)
        request.session['cart_items']=cart_obj.products.count()
    #  cart_obj.products.remove(obj) # to remove product
    #return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")


def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count()==0:
        return redirect("cart:home")      
    #else:
        #order_obj,new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    #user = request.user
    #billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_address_id = request.session.get("blling_address_id" ,None)
    shipping_address_id = request.session.get("shipping_address_id" ,  None)
    #billing_address_form = AddressForm() 
    billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request) 
    address_qs = None
    ## putting in model manager
    #guest_email_id = request.session.get('guest_email_id')
    #if user.is_authenticated:
     #   'logged in user checkout; remember payement stuff'
     #   billing_profile , billing_profile_created = BillingProfile.objects.get_or_create(user=user , email = user.email) 
    #elif guest_email_id is not None:
     #   'guest user checkout;auto reloads payment stuff'
      #  guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
       # billing_profile , billing_guest_profile_created = BillingProfile.objects.get_or_create( email = guest_email_obj.email)
    #else:
        #pass
    
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj,order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
        #order_qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        #if order_qs.count()==1:
            #order_obj = order_qs.first()
        #else:  
            #old_order_qs =  Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)  ### put in models.py of orders 
            #if old_order_qs.exists():
                #old_order_qs.update(active=False)
            #order_obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id= billing_address_id)
            del request.session["blling_address_id"] 
        if billing_address_id or shipping_address_id:
            order_obj.save()
    
    if request.method == "POST":
        " check that order is done "
        is_done = order_obj.check_done()
        #order_obj update to paid
        if is_done:
            order_obj.mark_paid() 
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")

    context = {
            "object" : order_obj ,
            "billing_profile" : billing_profile,
            "login_form" : login_form,
            "guest_form" : guest_form,
            "address_form" : address_form,
            "address_qs" : address_qs,
            #"billing_address_form" : billing_address_form
            }
    return render(request,"carts/checkout.html",context)





def checkout_done_view(request):
    return render(request,"carts/checkout-done.html",{})

