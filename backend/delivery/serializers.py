from rest_framework import serializers
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):

    customer = serializers.CharField(
        source="order.customer.username",
        read_only=True
    )

    order_total = serializers.DecimalField(
        source="order.total_amount",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Delivery
        fields = "__all__"