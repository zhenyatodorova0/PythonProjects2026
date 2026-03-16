from django.contrib import admin
from unfold.admin import ModelAdmin
from important_updates.models import Update


# Register your models here.
@admin.register(Update)
class UpdateAdmin(ModelAdmin):
    list_display = ["id", "title", "description", "liked_by"]

    @staticmethod
    def liked_by(obj) -> str:
        return ", ".join(update.title for update in obj.liked_by.all())
