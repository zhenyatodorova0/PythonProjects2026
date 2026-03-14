from django.urls import path

from feedback.views import FeedbackCreateView, FeedbackListView

app_name = "feedback"

urlpatterns = [
    path("", FeedbackListView.as_view(), name="list"),
    path("create/", FeedbackCreateView.as_view(), name="create"),
]
