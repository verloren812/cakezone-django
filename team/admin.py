from django.contrib import admin

from .models import Chef


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ("full_name", "designation", "experience_years", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "designation")
