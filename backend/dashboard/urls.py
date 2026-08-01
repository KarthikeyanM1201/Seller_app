from django.urls import path
from .views import SellerDashboardView

urlpatterns = [
    path(
        "",
        SellerDashboardView.as_view(),
        name="seller-dashboard",
    ),
]