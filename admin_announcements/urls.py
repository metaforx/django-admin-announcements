from django.urls import path

from . import views

app_name = "admin_announcements"

urlpatterns = [
    path("detail/<int:pk>/", views.announcement_detail, name="detail"),
]
