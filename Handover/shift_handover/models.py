from django.db import models

from shift_handover.choices import LanguageChoice


# Create your models here.
class ShiftHandover(models.Model):
    class TypeChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        INFORMATION = 'Information', 'Information'
        RISK = 'Risk', 'Risk'
        UPDATE = 'Update', 'Update'

    class StatusChoices(models.TextChoices):
        OPEN = 'Open', 'Open'
        IN_PROGRESS = 'In Progress', 'In Progress'
        BLOCKED = 'Blocked', 'Blocked'
        DONE = 'Done', 'Done'

    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
    )
    description = models.TextField()
    publishing_date = models.DateField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=10,
    )

class Post(models.Model):
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField()
    created_at = models.DateField(
        auto_now_add=True,
    )
    author = models.CharField(
        max_length=50,
    )
    language = models.CharField(
        choices=LanguageChoice.choices,
        default=LanguageChoice.OTHER,
    )