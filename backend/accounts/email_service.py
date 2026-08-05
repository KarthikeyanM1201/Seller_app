from django.core.mail import send_mail
from django.conf import settings


class EmailService:

    @staticmethod
    def send_order_confirmation(order):

        subject = f"Order #{order.id} Confirmation"

        message = f"""
Hello {order.customer.username},

Your order has been placed successfully.

Order ID : {order.id}

Total Amount : ₹{order.total_amount}

Thank you for shopping with us.
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer.email],
            fail_silently=False,
        )

    @staticmethod
    def send_payment_success(order):

        subject = f"Payment Successful - Order #{order.id}"

        message = f"""
    Hello {order.customer.username},

    Your payment has been received successfully.

    Order ID : {order.id}

    Amount : ₹{order.total_amount}

    Thank you for your purchase.
    """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer.email],
            fail_silently=False,
        )