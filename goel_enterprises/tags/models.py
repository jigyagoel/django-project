from django.db import models

from products.models import Product
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from app.utils import unique_slug_generator
# Create your models here.

class Tag(models.Model):
    title       = models.CharField( max_length =120)
    slug        = models.SlugField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product,blank=True)       ##foreign key


    def __str__(self):
        return self.title


def tag_pre_save_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance )

pre_save.connect(tag_pre_save_reciever,sender=Tag)
