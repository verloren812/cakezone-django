"""Context processor: shared data for the header and the footer of every page."""

from contact.models import ContactInfo
from menu.models import Category

from .models import Establishment


def site_context(request):
    """Adds the establishment info, the contacts and the menu categories to every template."""
    return {
        "site": Establishment.objects.filter(is_active=True).first(),
        "contacts": ContactInfo.objects.filter(is_active=True).first(),
        "menu_categories": Category.objects.filter(is_active=True),
    }
