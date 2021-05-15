from django.http import Http404
from django.views.generic import ListView,DetailView
from django.shortcuts import render,get_object_or_404
# Create your views here.

from carts.models import Cart
from .models import Product

class ProductFeaturedListView(ListView):
    template_name="products/list.html"
    def get_queryset(self,*args,**kwargs):
        return Product.objects.all().featured()



class ProductFeaturedDetailView(DetailView):
    template_name="products/featured-detail.html"
    queryset = Product.objects.all().featured()
    #def get_queryset(self,*args,**kwargs):
     #   return Product.objects.featured()



class ProductListView(ListView):                     ### class-based view
    #queryset = Product.objects.all()                 ### query set = model_name.objects.all()
    template_name ="products/list.html"

    #def get_context_data(self,*args,**kwargs):
        #context = super(ProductListView,self).get_context_data(*args,**kwargs)
        #print(context)
        #return context

    def get_queryset(self,*args,**kwargs):             ## responsible for view
        request=self.request
        return Product.objects.all()


def product_list_view(request):                      ### funtion - based view
    queryset = Product.objects.all()
    context={
         'object_list'  : queryset
            }
    return render (request, 'products/list.html',context)


class ProductDetailSlugView(DetailView):
    queryset=Product.objects.all()
    template_name="products/detail.html"

    
    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj = Cart.objects.new_or_get(self.request)
        context['cart']= cart_obj
        return context
         

    def get_object(self,*args,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug,active=True)
        except Product.DoesNotExist:
            raise Http404("NOt Found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug,active=True)
            instance = qs.first()
        except:
            raise Http404("Uhmm")
        return instance


class ProductDetailView(DetailView):                     ### class-based view
    #queryset = Product.objects.all()                 ### query set = model_name.objects.all()
    template_name ="products/detail.html"

    #def get_context_data(self,*args,**kwargs):
        #context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        #print(context)
        #return context


    def get_object(self,*args,**kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        
        instance=Product.objects.get_by_id(pk)
        #print(instance)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance


def product_detail_view(request,pk=None,*args,**kwargs):              ### funtion - based view
    #print(args)
    #print(kwargs)
    #instance = Product.objects.get(pk=pk)                             ### pk :primary key also called id
    #instance = get_object_or_404(Product,pk=pk)
    instance=Product.objects.get_by_id(pk)
    #print(instance)
    if instance is None:
        raise Http404("Product doesn't exist")
    #try:                                                             
        #instance=Product.objects.get(id=pk)
    #except Product.DoesNotExist:
        #print('no product here')
        #raise Http404("Product doesn't exist")
    #except:
        #print('huh!?')                                              
    
    #qs= Product.objects.filter(id=pk)                       
    #print(qs)
    #if qs.exists() and qs.count()==1:
        #instance = qs.first()
    #else:
        #raise Http404("Product doesn't exist")                       
    context={
         'object'  : instance
            }
    return render (request, 'products/detail.html',context)
