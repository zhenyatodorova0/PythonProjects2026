from django.db import models

# Create your models here.
class Feedback(models.Model):
    title = models.CharField(
        max_length=50
    )
    description = models.TextField()
    owner = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='feedback',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )