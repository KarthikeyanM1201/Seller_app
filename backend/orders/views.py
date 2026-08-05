from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Cart
from .serializers import CartSerializer, OrderSerializer
from products.models import Product
from django.db import transaction

from notifications.utils import create_notification
from .models import Order, OrderItem
from accounts.email_service import EmailService

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_item, created = Cart.objects.get_or_create(
            customer=request.user,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(
            customer=self.request.user
        )

class UpdateCartView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        cart_item = get_object_or_404(
            Cart,
            id=pk,
            customer=request.user
        )

        quantity = request.data.get("quantity")

        if quantity is None or int(quantity) <= 0:
            return Response(
                {"error": "Quantity must be greater than 0."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data)

class RemoveCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(
            Cart,
            id=pk,
            customer=request.user
        )

        cart_item.delete()

        return Response(
            {"message": "Item removed from cart."},
            status=status.HTTP_200_OK,
        )
        
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(
            customer=request.user
        ).delete()

        return Response(
            {"message": "Cart cleared successfully."},
            status=status.HTTP_200_OK,
        )

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        cart_items = Cart.objects.filter(customer=request.user)

        if not cart_items.exists():
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = 0

        order = Order.objects.create(
            customer=request.user,
            total_amount=0,
        )

        for item in cart_items:

            if item.quantity > item.product.stock:
                return Response(
                    {
                        "error": f"Only {item.product.stock} items available for {item.product.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            item.product.stock -= item.quantity
            item.product.save()

            total += item.product.price * item.quantity

        order.total_amount = total
        order.save()

        EmailService.send_order_confirmation(order)

        # Customer Notification
        create_notification(
            user=request.user,
            title="Order Placed",
            message=f"Your order #{order.id} has been placed successfully.",
            notification_type="order",
        )

        seller = order.order_items.first().product.seller

        create_notification(
            user=seller,
            title="New Order Received",
            message=f"You received a new order #{order.id}.",
            notification_type="order",
        )

        cart_items.delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).order_by("-created_at")

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        )

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk,
            customer=request.user
        )

        if order.status in [
            "shipped",
            "out_for_delivery",
            "delivered",
        ]:
            return Response(
                {
                    "error": "This order cannot be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.status == "cancelled":
            return Response(
                {
                    "message": "Order already cancelled."
                }
            )

        # Restore stock

        for item in order.items.all():

            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = "cancelled"
        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data)
