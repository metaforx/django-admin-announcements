from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/announcements/", include("admin_announcements.urls")),
    path("admin/", admin.site.urls),
]
