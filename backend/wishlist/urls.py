from django.urls import path

from .views import (
    AddWishlistView,
    WishlistListView,
    RemoveWishlistView,
)

urlpatterns = [
    path("", WishlistListView.as_view(), name="wishlist-list"),
    path("add/", AddWishlistView.as_view(), name="wishlist-add"),
    path("<int:pk>/remove/", RemoveWishlistView.as_view(), name="wishlist-remove"),
]