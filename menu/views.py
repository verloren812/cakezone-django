from django.shortcuts import get_object_or_404, render

from .models import Category


def index(request):
    """Menu and pricing page: all categories with their dishes."""
    context = {
        "categories": Category.objects.filter(is_active=True),
    }
    return render(request, "menu/menu_pricing.html", context)


def category(request, category):
    """A single menu category: the URL is parsed by a regular expression in urls.py."""
    selected = get_object_or_404(Category, slug=category, is_active=True)
    context = {
        "categories": Category.objects.filter(pk=selected.pk),
        "current_category": selected,
    }
    return render(request, "menu/menu_pricing.html", context)
