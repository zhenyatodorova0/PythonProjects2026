from django.test import TestCase
from django.urls import reverse

from feedback.models import Feedback
from important_updates.models import Update
from profiles.models import Profile
from tickets_handover.models import Ticket, TicketStatusHistory


class GlobalSearchViewTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            username="net_admin",
            email="net.admin@example.com",
        )
        Feedback.objects.create(
            title="Network latency",
            description="Latency on edge router",
            owner=self.profile,
        )
        update = Update.objects.create(
            title="Network maintenance",
            description="Planned work for core switch",
            category=Update.CategoryChoice.TECHNICAL_UPDATE,
            made_by=self.profile,
        )
        self.ticket = Ticket.objects.create(
            type=Ticket.Type.ACTION,
            ticket_id="NET_123",
            title="Network outage",
            description="Investigate outage",
            created_by=self.profile,
            status=Ticket.Status.OPEN,
        )
        TicketStatusHistory.objects.create(
            ticket=self.ticket, status="Network triage started"
        )
        update.liked_by.add(self.profile)

    def test_search_returns_results_from_all_apps(self):
        response = self.client.get(reverse("common:search"), data={"q": "net"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network latency")
        self.assertContains(response, "Network maintenance")
        self.assertContains(response, "net_admin")
        self.assertContains(response, "NET_123")
        self.assertEqual(response.context["total_results"], 4)

    def test_empty_query_returns_zero_results(self):
        response = self.client.get(reverse("common:search"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_results"], 0)
