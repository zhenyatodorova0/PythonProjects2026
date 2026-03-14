from django import forms
from django.db import models

from important_updates.models import Update


class UpdateBaseForm(forms.ModelForm):
    class Meta:
        model = Update
        exclude = ['liked_by']
        widgets = {
            "title": forms.TextInput(attrs={'placeholder': 'Title'}),
            "description": forms.Textarea(attrs={'placeholder': 'Description'}),
            "made_by": forms.HiddenInput(),
            "created_at": models.DateField(auto_now_add=True),
            "updated_at": models.DateField(auto_now=True),
        }
class UpdateCreateForm(UpdateBaseForm):
    ...

class UpdateEditForm(UpdateBaseForm):
    ...

class UpdateDeleteForm(UpdateBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
