import unicodedata
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as UserCreationFormDjango
)
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
        }


class AuthenticationAjaxForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True,
               'class': 'form-control'
               }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                'class': 'form-control'
            }
        ),
    )
