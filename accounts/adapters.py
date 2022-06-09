# project/users/adapter.py:
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth import socialaccount
from django.dispatch import receiver
from requests import request
from accounts.models import Account


from carts.models import Cart, CartItem
from carts.views import _cart_id
from allauth.account.signals import user_signed_up



@receiver(user_signed_up)
def retrieve_social_data(request, user, **kwargs):
    """Signal, that gets extra data from sociallogin and put it to profile."""
    # get the profile where i want to store the extra_data
    profile = Account(user=user)
    # in this signal I can retrieve the obj from SocialAccount
    data = SocialAccount.objects.filter(user=user, provider='google')
    # check if the user has signed up via social media
    if data:
        picture = data[0].get_avatar_url()
        if picture:
            # custom def to save the pic in the profile
            save_image_from_url(model=profile, url=picture)
        profile.save()