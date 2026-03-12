from django import forms

from shift_handover.choices import LanguageChoice


class Searchform(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
    )

class PostForm(forms.Form):
    title = forms.CharField(
        max_length=100,
    )
    content = forms.CharField(

    )
    author = forms.CharField(
        max_length=50,
    )
    language = forms.ChoiceField(
        choices=LanguageChoice.choices,
    )
