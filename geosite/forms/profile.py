from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            'password',
            'editor_for',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined',
            'groups',
            'user_permissions'
        )
