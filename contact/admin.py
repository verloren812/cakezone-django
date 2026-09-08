from django.contrib import admin

from .models import ContactInfo, ContactMessage


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("office_address", "email", "phone", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_processed",)
    date_hierarchy = "created_at"
    # what a visitor wrote must not be edited from the admin site
    readonly_fields = ("name", "email", "subject", "message", "created_at")
