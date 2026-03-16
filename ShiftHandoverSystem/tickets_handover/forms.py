from django import forms

from tickets_handover.models import Ticket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ["created_by", "created_at"]
        widgets = {
            "type": forms.Select(),
            "ticket_id": forms.TextInput(attrs={"placeholder": "Ticket ID"}),
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
            "status": forms.Select(),
        }


class TicketEditForm(TicketCreateForm): ...


class TicketDeleteForm(TicketCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.required = False
            field.widget.attrs["readonly"] = True
            field.widget.attrs["disabled"] = True


class TicketStatusForm(forms.Form):
    status_text = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Write status update"}),
    )
