from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class Pet(models.Model):
    name = models.CharField(
        max_length=30
    )
    personal_photo = models.URLField()
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
    )

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(f"{self.name}-{self.pk}")
        super().save(*args, **kwargs)

