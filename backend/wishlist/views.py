from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import Wishlist
from .serializers import WishlistSerializer

class AddWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product")

        product = get_object_or_404(
            Product,
            id=product_id
        )

        wishlist, created = Wishlist.objects.get_or_create(
            customer=request.user,
            product=product,
        )

        if not created:
            return Response(
                {"message": "Product already in wishlist."}
            )

        serializer = WishlistSerializer(wishlist)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(
            customer=self.request.user
        ).order_by("-created_at")

class RemoveWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        item = get_object_or_404(
            Wishlist,
            id=pk,
            customer=request.user
        )

        item.delete()

        return Response(
            {"message": "Removed from wishlist."},
            status=status.HTTP_200_OK
        )
    
