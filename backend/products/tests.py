from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from products.models import Category


class ProductTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="seller@gmail.com",
            email="seller@gmail.com",
            password="Seller123",
            role="seller",
            is_verified=True,
        )

        self.category = Category.objects.create(
            name="Electronics"
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "seller@gmail.com",
                "password": "Seller123",
            },
            format="json",
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.data)

        token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_create_product(self):

        response = self.client.post(
            "/api/products/",
            {
                "category": self.category.id,
                "name": "Laptop",
                "description": "Gaming Laptop",
                "price": 65000,
                "stock": 5,
                "weight": "2 Kg",
                "is_available": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )