from django.db import models

from store.models import Product





class Wishlist(models.Model):


    wishlist_id = models.CharField(max_length=250,blank=True,null=True)
    date_added =models.DateTimeField(auto_now_add=True)



    def __str__(self):

        return self.wishlist_id




class WishlistItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)       
    is_active = models.BooleanField(default=True)



    def __str__(self):

        return self.product.product_name

