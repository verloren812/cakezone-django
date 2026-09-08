"""Form of the Contact Us page."""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage

# Bootstrap classes of the template, so the form looks like the rest of the page.
INPUT_ATTRS = {"class": "form-control bg-light border-0 px-4", "style": "height: 55px;"}
TEXTAREA_ATTRS = {"class": "form-control bg-light border-0 px-4 py-3", "rows": 4}


class ContactMessageForm(forms.ModelForm):
    """Creates a ContactMessage record from the data of the page form."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs=INPUT_ATTRS | {"placeholder": _("Your Name")}),
            "email": forms.EmailInput(attrs=INPUT_ATTRS | {"placeholder": _("Your Email")}),
            "subject": forms.TextInput(attrs=INPUT_ATTRS | {"placeholder": _("Subject")}),
            "message": forms.Textarea(attrs=TEXTAREA_ATTRS | {"placeholder": _("Message")}),
        }

    def clean_message(self):
        """Rejects messages that are too short to be a real request."""
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(_("Please describe your request in more detail."))
        return message
