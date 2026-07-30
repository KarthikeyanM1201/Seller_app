from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import OTP
from .utils import generate_otp

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
            "phone",
            "password",
            "role",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        email = validated_data["email"]

        user = User(
            username=email,
            **validated_data
        )

        user.set_password(password)
        user.save()

        otp = generate_otp()

        OTP.objects.create(
            phone=user.phone,
            otp=otp,
        )

        # Development only
        user.generated_otp = otp

        return user

class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "role",
            "is_verified",
        ]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        print("EMAIL:", email)
        print("PASSWORD:", password)

        user = authenticate(
            username=email,
            password=password
        )

        print("AUTH USER:", user)

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_verified:
            raise serializers.ValidationError(
                "Please verify your phone number before logging in."
            )

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }

class OTPVerifySerializer(serializers.Serializer):

    phone = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, attrs):

        phone = attrs["phone"]
        otp = attrs["otp"]

        try:
            otp_obj = OTP.objects.get(
                phone=phone,
                otp=otp
            )
        except OTP.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid OTP."
            )

        if timezone.now() > otp_obj.expires_at:
            raise serializers.ValidationError(
                "OTP has expired."
            )

        user = User.objects.get(phone=phone)

        user.is_verified = True
        user.save()

        otp_obj.delete()

        return {
            "message": "Phone verified successfully."
        }