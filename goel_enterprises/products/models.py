import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from app.utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext= os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,3798488387)
    name , ext = get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename = new_filename,ext=ext)     ##if using python 3.6 can do f'{new_filename}{ext}'
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)
# Create your models here.


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True,active=True)
    def active(self):
        return self.filter(active=True)
    def search(self,query):
        lookups = (
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(price__icontains=query) |
                Q(tag__title__icontains=query)
                )
        
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):                   ## this is not overriding our objects model manager just extending it
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)
    def featured(self):
        return self.get_queryset().featured()
    def all(self):
        return self.get_queryset().active()
    def get_by_id(self,id):
        qs= self.get_queryset().filter(id=id)            ## Product.objects== self.get_queryset()
        if qs.count()==1:
            return qs.first()
        return None
    def search(self,query): 
        return self.get_queryset().active().search(query)

class Product (models.Model):
    title = models.CharField(max_length = 120)
    slug = models.SlugField(blank=True,default="Abc",unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=20,default=39.99 )
    image = models.FileField(upload_to=upload_image_path,null=True,blank=True)
    featured = models.BooleanField(default= False)
    active = models.BooleanField(default= True)
    timestamp = models.DateTimeField(auto_now_add=True)


    objects=ProductManager()           

    def get_absolute_url(self):                      ## get back to url
        #return "/goel_enterprises/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail",kwargs={"slug":self.slug})   

    def __str__(self):                              # will change product object name to tiltle in database in python 3 .
        return self.title

    #property
    def name(self):            ### just incase mess up with title with name anywhere
        return self.title


def product_pre_save_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance )

pre_save.connect(product_pre_save_reciever,sender=Product)
