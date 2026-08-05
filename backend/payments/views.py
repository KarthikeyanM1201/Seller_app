import razorpay
from rest_framework import generics
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.utils import create_notification
from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer
from accounts.email_service import EmailService

#Razorpay client
client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)

class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get("order_id")

        order = get_object_or_404(
            Order,
            id=order_id,
            customer=request.user
        )

        amount = int(order.total_amount * 100)

        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_amount,
            razorpay_order_id=razorpay_order["id"],
            status="Pending"
        )

        serializer = PaymentSerializer(payment)

        return Response(
            {
                "message": "Payment order created successfully.",
                "payment": serializer.data,
                "razorpay": razorpay_order,
                "key": settings.RAZORPAY_KEY_ID,
            },
            status=status.HTTP_201_CREATED
        )

class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })

            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = "Success"
            payment.save()

            # Update order status
            payment.order.status = "confirmed"
            payment.order.save()

            create_notification(
                user=payment.user,
                title="Payment Successful",
                message=f"Payment for Order #{payment.order.id} was successful.",
                notification_type="payment",
            )

            EmailService.send_payment_success(payment.order)

            return Response(
                {
                    "success": True,
                    "message": "Payment verified successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            try:
                payment = Payment.objects.get(
                    razorpay_order_id=razorpay_order_id
                )
                payment.status = "Failed"
                payment.save()
            except Payment.DoesNotExist:
                pass

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class PaymentHistoryView(generics.ListAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            user=self.request.user
        ).order_by("-created_at")