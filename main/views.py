from django.shortcuts import render

from menu.models import Dish

from .models import Establishment, Testimonial


def index(request):
    """Home page: establishment information, client testimonials and popular cakes."""
    context = {
        "establishment": Establishment.objects.filter(is_active=True).first(),
        "testimonials": Testimonial.objects.filter(is_published=True),
        "popular_dishes": Dish.objects.filter(is_active=True)[:6],
    }
    return render(request, "main/home.html", context)
