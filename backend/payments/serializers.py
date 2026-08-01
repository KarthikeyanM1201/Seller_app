from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(
        source="user.username",
        read_only=True
    )

    order_id = serializers.IntegerField(
        source="order.id",
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "customer",
            "order_id",
            "amount",
            "status",
            "razorpay_order_id",
            "razorpay_payment_id",
            "created_at",
        ]