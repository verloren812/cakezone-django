from django.contrib import admin

from .models import Establishment, Testimonial


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name", "years_of_experience", "happy_clients", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "profession", "rating", "is_published", "created_at")
    list_filter = ("is_published", "rating")
    search_fields = ("author_name", "text")
