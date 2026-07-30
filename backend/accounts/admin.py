from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTP


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone",
                    "role",
                    "is_verified",
                    "profile_image",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "phone",
        "role",
        "is_verified",
        "is_staff",
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "otp",
        "created_at",
        "expires_at",
    )