from django.db import models


class Service(models.Model):
    """A service provided by the establishment (a card on the Our Service page)."""

    title = models.CharField("service title", max_length=150)
    description = models.TextField("description")
    icon = models.CharField(
        "icon css class", max_length=50, blank=True,
        help_text="for example, bi bi-cake",
    )
    image = models.ImageField("image", upload_to="services/", blank=True)
    price_from = models.DecimalField(
        "price from", max_digits=8, decimal_places=2, null=True, blank=True
    )
    order = models.PositiveSmallIntegerField("display order", default=0)
    is_active = models.BooleanField("show on the site", default=True)

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
