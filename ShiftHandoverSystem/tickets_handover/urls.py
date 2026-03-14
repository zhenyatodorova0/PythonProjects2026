from django.urls import path

from tickets_handover.views import (
    TicketHandoverCreateView,
    TicketHandoverDeleteView,
    TicketHandoverEditView,
    TicketHandoverListView,
    TicketHandoverStatusView,
)

app_name = "tickets_handover"

urlpatterns = [
    path("", TicketHandoverListView.as_view(), name="list"),
    path("create/", TicketHandoverCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", TicketHandoverEditView.as_view(), name="edit"),
    path("delete/<int:pk>/", TicketHandoverDeleteView.as_view(), name="delete"),
    path("status/<int:pk>/", TicketHandoverStatusView.as_view(), name="status"),
]
