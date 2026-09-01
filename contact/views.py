from django.shortcuts import render

from .models import ContactInfo


def index(request):
    """Contact Us page: the contact information of the establishment."""
    context = {
        "contact_info": ContactInfo.objects.filter(is_active=True).first(),
    }
    return render(request, "contact/contact_us.html", context)
