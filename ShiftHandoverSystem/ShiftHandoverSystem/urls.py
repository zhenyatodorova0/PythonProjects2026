from django.contrib import admin
from django.urls import path, include

import profiles

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.urls")),
    path("", include("profiles.urls")),
    path("handover/", include("tickets_handover.urls")),
    path("important_updates/", include("important_updates.urls")),
    path("feedback/", include("feedback.urls")),
]

handler404 = "common.views.custom_page_not_found"
