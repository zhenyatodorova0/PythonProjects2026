from django.test import TestCase
from django.urls import reverse

from profiles.models import Profile
from tickets_handover.models import Ticket, TicketStatusHistory


class TicketHandoverStatusViewTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(username="tester")

    def _create_ticket(self, status: str) -> Ticket:
        return Ticket.objects.create(
            type=Ticket.Type.ACTION,
            ticket_id=f"T_{status.replace(' ', '_')}",
            title=f"{status} ticket",
            description="desc",
            created_by=self.profile,
            status=status,
        )

    def test_cannot_add_current_status_when_ticket_is_done(self):
        ticket = self._create_ticket(Ticket.Status.DONE)

        response = self.client.post(
            reverse("tickets_handover:status", kwargs={"pk": ticket.pk}),
            data={"status_text": "Extra update after done"},
        )

        self.assertRedirects(response, reverse("tickets_handover:list"))
        self.assertFalse(
            TicketStatusHistory.objects.filter(
                ticket=ticket, status="Extra update after done"
            ).exists()
        )

    def test_can_add_current_status_when_ticket_is_not_done(self):
        ticket = self._create_ticket(Ticket.Status.OPEN)

        response = self.client.post(
            reverse("tickets_handover:status", kwargs={"pk": ticket.pk}),
            data={"status_text": "Work started"},
        )

        self.assertRedirects(response, reverse("tickets_handover:list"))
        self.assertTrue(
            TicketStatusHistory.objects.filter(
                ticket=ticket, status="Work started"
            ).exists()
        )
