from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):

    category_name =  models.CharField(max_length=20,unique=True)
    slug = models.SlugField(max_length=100,unique=True,null=True)
    category_image = models.ImageField(upload_to='photos/category',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):

        return reverse('products_by_category',args=[self.slug])    

    def __str__(self) :
        return self.category_name

