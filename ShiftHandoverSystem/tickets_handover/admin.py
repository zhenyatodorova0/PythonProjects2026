from django.contrib import admin
from unfold.admin import ModelAdmin
from tickets_handover.models import Ticket


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ["ticket_id", "description", "status"]
