from django.urls import path
from .views import (
    AddToCartView,
    CancelOrderView,
    CartListView,
    OrderDetailView,
    OrderListView,
    UpdateCartView,
    RemoveCartView,
    ClearCartView,
    CheckoutView

)

urlpatterns = [

    #cart management
    path("", CartListView.as_view(), name="cart-list"),
    path("add/", AddToCartView.as_view(), name="cart-add"),
    path("<int:pk>/update/", UpdateCartView.as_view(), name="cart-update"),
    path("<int:pk>/remove/", RemoveCartView.as_view(), name="cart-remove"),
    path("clear/", ClearCartView.as_view(), name="cart-clear"),
    
    #checkout
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    #order management
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/cancel/", CancelOrderView.as_view(), name="cancel-order"),
]