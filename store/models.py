
from distutils.command.upload import upload
from email.mime import image
from itertools import product
from django.urls import reverse
from accounts.models import Account
from category.models import Category
from django.db import models




class Product(models.Model):

    product_name = models.CharField(max_length=250,unique=True)

    slug         = models.SlugField(max_length=250,unique=True)

    description  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    stock        = models.IntegerField()
    image        = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=False)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    rating_dummy = models.IntegerField(null=True)


    def get_url(self):

        return reverse('product_details',args=[self.category.slug,self.slug])


    def __str__(self):

        return self.product_name


class ProductImage(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to = 'photos/products/extras')

    def __str__(self):

        return self.product.product_name       
class Review(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    content = models.TextField(max_length=500,null=True)
    rating = models.IntegerField(null=True)  
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):

        return self.user.email       
