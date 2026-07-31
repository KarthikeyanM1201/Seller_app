from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)
from .permissions import IsSeller


class CategoryListCreateView(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = [
        "category",
        "seller",
        "is_available",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "price",
        "created_at",
    ]

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        if self.request.user.role != "seller":
            raise PermissionDenied(
                "Only sellers can add products."
            )

        serializer.save(
            seller=self.request.user
        )

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user
        )