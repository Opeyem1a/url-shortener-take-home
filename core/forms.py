from django import forms
from django.core.exceptions import ValidationError

from core.models import Url

from gettext import gettext as _


class UrlForm(forms.Form):
    url = forms.URLField(required=True, max_length=255)
    custom_hash = forms.CharField(required=False, max_length=25)

    def clean_custom_hash(self):
        custom_hash = self.cleaned_data["custom_hash"]
        if Url.objects.filter(hashed_url=custom_hash).exists():
            raise ValidationError(_("This short url code is already taken. Please try another."))

        return custom_hash
