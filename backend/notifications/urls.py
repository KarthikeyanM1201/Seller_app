from django.urls import path

from .views import (
    NotificationListView,
    MarkNotificationReadView,
    UnreadNotificationCountView,
)

urlpatterns = [

    path(
        "",
        NotificationListView.as_view(),
        name="notification-list",
    ),

    path(
        "<int:pk>/read/",
        MarkNotificationReadView.as_view(),
        name="notification-read",
    ),

    path(
        "unread-count/",
        UnreadNotificationCountView.as_view(),
        name="notification-count",
    ),
]