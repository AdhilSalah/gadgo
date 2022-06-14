from django.contrib import admin


from accounts.models import Account, ShippingAddress

# Register your models here.
admin.site.register(Account)
admin.site.register(ShippingAddress)

