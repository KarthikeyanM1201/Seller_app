from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OTPVerifySerializer, RegisterSerializer, LoginSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
            {
                "success": True,
                "message": "Registration successful.",
                "otp": user.generated_otp
            },
            status=status.HTTP_201_CREATED
            )

        return Response(    
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)

class VerifyOTPView(APIView):

    def post(self, request):

        serializer = OTPVerifySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )
