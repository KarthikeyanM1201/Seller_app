from django.db import models
from django.conf import settings
from orders.models import Order


class Delivery(models.Model):

    STATUS_CHOICES = [
        ("assigned", "Assigned"),
        ("accepted", "Accepted"),
        ("picked_up", "Picked Up"),
        ("out_for_delivery", "Out For Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery",
    )

    delivery_partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "delivery"},
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="assigned",
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
    )

    picked_up_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    delivered_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Delivery #{self.order.id}"