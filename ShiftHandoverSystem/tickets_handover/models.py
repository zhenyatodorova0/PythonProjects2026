from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from profiles.models import Profile


# Create your models here.
class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "Open", "Open",
        IN_PROGRESS = "In Progress", "In Progress",
        BLOCKED = "Blocked", "Blocked",
        DONE = "Done", "Done",

    class Type(models.TextChoices):
        ACTION = "Action", "Action",
        DISCUSSION = "Discussion", "Discussion",
        QUESTION = "Question", "Question",
        REVIEW = "Review", "Review",
        UPDATE = "Update", "Update",
        INFORMATION = "Information", "Information",

    type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    ticket_id = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[A-Za-z0-9_]+$',
            )
        ]
    )
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name="ticket_created_by",
    )
    # shift = models.ForeignKey(
    #     "Shift", on_delete=models.CASCADE
    # )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
    )