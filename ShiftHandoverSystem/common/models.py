from django.db import models

# Create your models here.

# Create your models here.
class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

class Like(models.Model):
    to_photo = models.ForeignKey(
        "important_updates.Update",
        on_delete=models.CASCADE,
    )