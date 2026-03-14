from django import forms

from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            "username": forms.TextInput(
                attrs={'placeholder': 'Username'}
            ),
            "email": forms.EmailInput(
                attrs={'placeholder': 'Email'}
            ),
            "password": forms.PasswordInput(
                attrs={'placeholder': 'Password'}
            )
        }
