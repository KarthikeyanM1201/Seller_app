from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_products = serializers.IntegerField()

    total_orders = serializers.IntegerField()

    total_revenue = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    pending_orders = serializers.IntegerField()

    low_stock_products = serializers.IntegerField()

    recent_orders = serializers.ListField()