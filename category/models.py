from distutils.command.upload import upload
from tabnanny import verbose
from unicodedata import category
from django.db import models

# Create your models here.

class category(models.Model):

    category_name =  models.CharField(max_length=20,unique=True)
    slug = models.SlugField(max_length=100,unique=True,null=True)
    category_image = models.ImageField(upload_to='photos/category',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) :
        return self.category_name

