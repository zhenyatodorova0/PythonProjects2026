from django.db import models

# Create your models here.
class Update(models.Model):
    title = models.CharField(
        max_length=200
    )
    description = models.TextField()
    # made_by = models.ForeignKey(
    #     User, on_delete=models.CASCADE
    # )
    # shift = models.ForeignKey(
    #     "Shift", on_delete=models.CASCADE
    # )
    created_at = models.DateTimeField(
        auto_now_add=True
    )