from datetime import timedelta

from django.utils import timezone

from feedback.models import Feedback
from important_updates.models import Update
from profiles.models import Profile
from tickets_handover.models import Ticket, TicketStatusHistory


def get_or_create_profile(username, email, password):
    profile, created = Profile.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "password": password,
        },
    )
    if not created:
        changed = False
        if profile.email != email:
            profile.email = email
            changed = True
        if profile.password != password:
            profile.password = password
            changed = True
        if changed:
            profile.save(update_fields=["email", "password"])
    return profile, created


def set_created_at(instance, dt):
    instance.__class__.objects.filter(pk=instance.pk).update(created_at=dt)


def ensure_status_history(ticket, statuses):
    existing = set(ticket.status_entries.values_list("status", flat=True))
    for status in statuses:
        if status not in existing:
            TicketStatusHistory.objects.create(ticket=ticket, status=status)


def ensure_ticket(
    *, profile, ticket_id, ticket_type, title, description, status, history
):
    ticket, created = Ticket.objects.get_or_create(
        ticket_id=ticket_id,
        defaults={
            "type": ticket_type,
            "title": title,
            "description": description,
            "created_by": profile,
            "status": status,
        },
    )
    if not created:
        changed = False
        for field, value in {
            "type": ticket_type,
            "title": title,
            "description": description,
            "created_by": profile,
            "status": status,
        }.items():
            if getattr(ticket, field) != value:
                setattr(ticket, field, value)
                changed = True
        if changed:
            ticket.save()
    ensure_status_history(ticket, history)
    return ticket, created


def ensure_update(*, profile, title, description, category, created_at, liked_by=None):
    update, created = Update.objects.get_or_create(
        title=title,
        defaults={
            "description": description,
            "category": category,
            "made_by": profile,
        },
    )
    if not created:
        changed = False
        for field, value in {
            "description": description,
            "category": category,
            "made_by": profile,
        }.items():
            if getattr(update, field) != value:
                setattr(update, field, value)
                changed = True
        if changed:
            update.save()
    set_created_at(update, created_at)
    if liked_by:
        update.liked_by.set(liked_by)
    return update, created


def ensure_feedback(*, profile, title, description, created_at):
    feedback, created = Feedback.objects.get_or_create(
        owner=profile,
        title=title,
        defaults={"description": description},
    )
    if not created and feedback.description != description:
        feedback.description = description
        feedback.save(update_fields=["description"])
    set_created_at(feedback, created_at)
    return feedback, created


now = timezone.now()

primary_profile = Profile.objects.order_by("pk").first()
if primary_profile is None:
    primary_profile, primary_created = get_or_create_profile(
        username="shift_lead",
        email="shift.lead@example.com",
        password="handoverpass123",
    )
else:
    primary_created = False
    if not primary_profile.email:
        primary_profile.email = "shift.lead@example.com"
    if not primary_profile.password:
        primary_profile.password = "handoverpass123"
    primary_profile.save(update_fields=["email", "password"])

backup_profile, backup_created = get_or_create_profile(
    username="core_team",
    email="core.team@example.com",
    password="coreteam123",
)
weekend_profile, weekend_created = get_or_create_profile(
    username="weekend_shift",
    email="weekend.shift@example.com",
    password="weekend123",
)

tickets = [
    {
        "ticket_id": "DB_4812",
        "ticket_type": Ticket.Type.ACTION,
        "title": "Investigate overnight replication lag",
        "description": "Primary node is 7 minutes behind on EU analytics replication. Verify backlog trend and escalate if delay exceeds 10 minutes.",
        "status": Ticket.Status.IN_PROGRESS,
        "history": [
            "Replication lag alert acknowledged by evening shift.",
            "Lag dropped from 11 minutes to 7 minutes after queue drain.",
            "Morning shift should confirm replication is stable after backup window.",
        ],
    },
    {
        "ticket_id": "OPS_7701",
        "ticket_type": Ticket.Type.REVIEW,
        "title": "Review failed restart on batch worker node",
        "description": "One worker node did not rejoin after scheduled restart. Logs show stale lock cleanup may be required before next retry.",
        "status": Ticket.Status.BLOCKED,
        "history": [
            "Restart attempted at 02:15 UTC but node remained unhealthy.",
            "Temporary workaround is to keep the node drained from the pool.",
            "Next shift should coordinate with platform team for safe cleanup.",
        ],
    },
    {
        "ticket_id": "NET_2450",
        "ticket_type": Ticket.Type.INFORMATION,
        "title": "Monitor packet loss on backup MPLS path",
        "description": "Intermittent packet loss was observed on the backup carrier path during failover testing. Continue monitoring while primary path remains stable.",
        "status": Ticket.Status.OPEN,
        "history": [
            "Loss observed only during test traffic bursts.",
            "Carrier ticket opened and waiting for callback.",
        ],
    },
]

updates = [
    {
        "title": "Core database maintenance completed",
        "description": "Index rebuild on the incident reporting cluster finished successfully. Query latency returned to baseline and no follow-up action is required.",
        "category": Update.CategoryChoice.TECHNICAL_UPDATE,
        "created_at": now - timedelta(days=1, hours=2),
        "liked_by": [backup_profile, weekend_profile],
    },
    {
        "title": "New handover checklist published for weekend shifts",
        "description": "Weekend teams should now confirm alert ownership, open escalations, and rollback plans before ending the shift. The checklist is effective immediately.",
        "category": Update.CategoryChoice.PROCEDURE_UPDATE,
        "created_at": now - timedelta(days=2, hours=4),
        "liked_by": [backup_profile],
    },
    {
        "title": "Storage alert thresholds tuned after false positives",
        "description": "Noise from temporary snapshot growth has been reduced. Continue to watch for sustained usage spikes on the finance volume group.",
        "category": Update.CategoryChoice.TECHNICAL_UPDATE,
        "created_at": now - timedelta(days=4, hours=1),
        "liked_by": [weekend_profile],
    },
    {
        "title": "Escalation bridge contact list refreshed",
        "description": "Updated conference bridge owners and fallback contacts were added for database, platform, and network incidents.",
        "category": Update.CategoryChoice.OTHER,
        "created_at": now - timedelta(days=6, hours=3),
        "liked_by": [backup_profile, weekend_profile],
    },
]

feedback_items = [
    {
        "title": "Night shift outage summary",
        "description": "The latest incident summary was clear and helped the morning shift resume investigation without repeating validation steps.",
        "created_at": now - timedelta(days=1, hours=5),
    },
    {
        "title": "Handover notes format",
        "description": "The current ticket notes are easier to scan when pending actions are listed first and ownership is explicit.",
        "created_at": now - timedelta(days=3, hours=6),
    },
    {
        "title": "Update visibility",
        "description": "Important updates are much easier to track when procedure changes are posted before the weekend handover begins.",
        "created_at": now - timedelta(days=5, hours=2),
    },
]

ticket_results = [ensure_ticket(profile=primary_profile, **item) for item in tickets]
update_results = [ensure_update(profile=primary_profile, **item) for item in updates]
feedback_results = [
    ensure_feedback(profile=primary_profile, **item) for item in feedback_items
]

print("Demo data ready.")
print(
    f"Profiles: primary={primary_profile.username} "
    f"(created={primary_created}), backup_created={backup_created}, weekend_created={weekend_created}"
)
print(
    f"Tickets: total={len(ticket_results)}, created={sum(1 for _, created in ticket_results if created)}"
)
print(
    f"Updates: total={len(update_results)}, created={sum(1 for _, created in update_results if created)}"
)
print(
    f"Feedback: total={len(feedback_results)}, created={sum(1 for _, created in feedback_results if created)}"
)
