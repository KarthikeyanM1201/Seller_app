from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from orders.models import Order


class SellerDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        seller = request.user

        products = Product.objects.filter(
            seller=seller
        )

        total_products = products.count()

        total_orders = Order.objects.filter(
            items__product__seller=seller
        ).distinct().count()

        total_revenue = (
            Order.objects.filter(
                items__product__seller=seller,
                status="delivered",
            ).aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )

        pending_orders = Order.objects.filter(
            items__product__seller=seller,
            status="pending",
        ).distinct().count()

        low_stock_products = products.filter(
            stock__lte=5
        ).count()

        recent_orders = Order.objects.filter(
            items__product__seller=seller
        ).distinct().order_by("-created_at")[:5]

        recent_orders_data = []

        for order in recent_orders:
            recent_orders_data.append({
                "id": order.id,
                "customer": order.customer.username,
                "amount": order.total_amount,
                "status": order.status,
            })

        return Response({
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "pending_orders": pending_orders,
            "low_stock_products": low_stock_products,
            "recent_orders": recent_orders_data,
        })