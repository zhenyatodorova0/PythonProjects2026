from django.db import models

# Create your models here.
class Update(models.Model):
    class CategoryChoice(models.TextChoices):
        TECHNICAL_UPDATE = "Technical Update", "Technical Update"
        PROCEDURE_UPDATE = "Procedure Update", "Procedure Update"
        OTHER = "Other", "Other"

    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    category = models.CharField(
        max_length=30,
        choices=CategoryChoice.choices,
    )
    made_by = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='updates_made_by',
    )
    # shift = models.ForeignKey(
    #     "Shift", on_delete=models.CASCADE
    # )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def category_image(self):
        images = {
            self.CategoryChoice.TECHNICAL_UPDATE: "images/technical_update.png",
            self.CategoryChoice.PROCEDURE_UPDATE: "images/procedure_update.png",
            self.CategoryChoice.OTHER: "images/other_update.png",
        }
        return images.get(self.category, "images/default_update.png")