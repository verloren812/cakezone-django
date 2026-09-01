from django.shortcuts import render

from .models import Chef


def index(request):
    """Master Chefs page: the chef cards."""
    context = {
        "chefs": Chef.objects.filter(is_active=True),
    }
    return render(request, "team/master_chefs.html", context)
