from django.urls import path
from .views import (
    AcceptDeliveryView,
    DeliveryListView,
    DeliveryDetailView,
    AssignDeliveryView,
    MyDeliveriesView,
    UpdateDeliveryStatusView,
)

urlpatterns = [

    path("", DeliveryListView.as_view()),

    path("mine/", MyDeliveriesView.as_view()),

    path(
        "assign/<int:order_id>/",
        AssignDeliveryView.as_view(),
    ),

    path(
        "<int:pk>/",
        DeliveryDetailView.as_view(),
    ),

    path(
        "<int:pk>/accept/",
        AcceptDeliveryView.as_view(),
    ),

    path(
        "<int:pk>/status/",
        UpdateDeliveryStatusView.as_view(),
    ),
]