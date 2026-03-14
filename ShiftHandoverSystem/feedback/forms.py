from django import forms

from feedback.models import Feedback


class FeedbackCreateForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ["owner", "created_at"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }
