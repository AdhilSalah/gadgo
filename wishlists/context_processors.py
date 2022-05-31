


from wishlists.models import Wishlist, WishlistItem
from .views import _wishlist_id


def counter(request):

    wishlist_count = 0


    try:

        wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])

        for wishlist_item in wishlist_items:

            wishlist_count += 1

    except Wishlist.DoesNotExist:
        wishlist_count=0 

    return dict(wishlist_count=wishlist_count) 