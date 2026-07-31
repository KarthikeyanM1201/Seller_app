from django.urls import path

from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ProductDetailView,
)

urlpatterns = [

    path(
        "categories/",
        CategoryListCreateView.as_view(),
    ),

    path(
        "",
        ProductListCreateView.as_view(),
    ),

    path(
        "<int:pk>/",
        ProductDetailView.as_view(),
    ),

]