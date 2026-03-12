from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

# Create your models here.
class Ticket(models.Model):
    status = models.CharField(
        max_length=50
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
    description = models.TextField()

    priority = models.CharField(
        max_length=20
    )

    # created_by = models.ForeignKey(
    #     User, on_delete=models.CASCADE
    # )
    # shift = models.ForeignKey(
    #     "Shift", on_delete=models.CASCADE
    # )
    created_at = models.DateTimeField(
        auto_now_add=True
    )