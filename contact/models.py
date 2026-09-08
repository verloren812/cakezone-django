from django.db import models


class ContactInfo(models.Model):
    """Contact information of the establishment (the Contact Us page and the footer)."""

    office_address = models.CharField("office address", max_length=250)
    email = models.EmailField("email")
    phone = models.CharField("phone", max_length=30)

    working_hours_weekdays = models.CharField(
        "working hours on weekdays", max_length=100, blank=True, default="09:00 - 19:00"
    )
    working_hours_weekend = models.CharField(
        "working hours on weekend", max_length=100, blank=True, default="10:00 - 17:00"
    )

    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    twitter = models.URLField("Twitter", blank=True)
    map_embed = models.TextField("map embed code", blank=True)

    is_active = models.BooleanField("primary contact", default=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    class Meta:
        verbose_name = "contact information"
        verbose_name_plural = "contact information"

    def __str__(self):
        return "Contacts: " + self.office_address


class ContactMessage(models.Model):
    """A message sent through the form on the Contact Us page."""

    name = models.CharField("name", max_length=100)
    email = models.EmailField("email")
    subject = models.CharField("subject", max_length=150)
    message = models.TextField("message")

    created_at = models.DateTimeField("received at", auto_now_add=True)
    is_processed = models.BooleanField("processed", default=False)

    class Meta:
        verbose_name = "message from the form"
        verbose_name_plural = "messages from the form"
        ordering = ["-created_at"]

    def __str__(self):
        return "%s - %s" % (self.name, self.subject)
