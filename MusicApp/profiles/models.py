from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r"^[A-z0-9_]+$",
                message="Ensure this value contains only letters, numbers, and underscore."
            )
        ]
    )
    email = models.EmailField()
    age = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
        ]
    )