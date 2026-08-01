from django.urls import path

from .views import (
    CreatePaymentView,
    VerifyPaymentView,
    PaymentHistoryView,
)

urlpatterns = [
    path(
        "create/",
        CreatePaymentView.as_view(),
        name="payment-create",
    ),

    path(
        "verify/",
        VerifyPaymentView.as_view(),
        name="payment-verify",
    ),

    path(
        "history/",
        PaymentHistoryView.as_view(),
        name="payment-history",
    ),
]