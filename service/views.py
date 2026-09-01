from django.shortcuts import render

from .models import Service


def index(request):
    """Our Service page: the services of the establishment."""
    context = {
        "services": Service.objects.filter(is_active=True),
    }
    return render(request, "service/our_service.html", context)
