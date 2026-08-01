from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Delivery
from .serializers import DeliverySerializer
from orders.models import Order
from accounts.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class AssignDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        order = get_object_or_404(Order, id=order_id)

        delivery_partner_id = request.data.get("delivery_partner")

        partner = get_object_or_404(
            User,
            id=delivery_partner_id,
            role="delivery",
        )

        delivery = Delivery.objects.create(
            order=order,
            delivery_partner=partner,
        )

        serializer = DeliverySerializer(delivery)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class DeliveryListView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Delivery.objects.all().order_by("-assigned_at")

class DeliveryDetailView(generics.RetrieveAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    queryset = Delivery.objects.all()

class MyDeliveriesView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Delivery.objects.filter(
            delivery_partner=self.request.user
        ).order_by("-assigned_at")


class AcceptDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        delivery = get_object_or_404(
            Delivery,
            id=pk,
            delivery_partner=request.user
        )

        delivery.status = "accepted"
        delivery.save()

        return Response({
            "message": "Delivery accepted successfully."
        })

class UpdateDeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        delivery = get_object_or_404(
            Delivery,
            id=pk,
            delivery_partner=request.user
        )

        status_value = request.data.get("status")

        allowed = [
            "picked_up_at",
            "out_for_delivery",
            "delivered_at",
        ]

        if status_value not in allowed:
            return Response(
                {
                    "error": "Invalid status."
                },
                status=400,
            )

        delivery.status = status_value
        delivery.save()

        return Response({
            "message": "Status updated successfully."
        })