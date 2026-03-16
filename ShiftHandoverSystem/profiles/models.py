from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


# Create your models here.
class Profile(models.Model):
    username = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$",
                message="Enter a valid username.",
            ),
        ],
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
