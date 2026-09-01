from django.db import models


class Chef(models.Model):
    """A master chef (a card on the Master Chefs page)."""

    full_name = models.CharField("full name", max_length=150)
    designation = models.CharField("designation", max_length=100)
    photo = models.ImageField("photo", upload_to="chefs/", blank=True)
    biography = models.TextField("biography", blank=True)
    experience_years = models.PositiveSmallIntegerField("experience, years", default=0)

    twitter = models.URLField("Twitter", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)

    order = models.PositiveSmallIntegerField("display order", default=0)
    is_active = models.BooleanField("show on the site", default=True)

    class Meta:
        verbose_name = "chef"
        verbose_name_plural = "chefs"
        ordering = ["order", "full_name"]

    def __str__(self):
        return "%s - %s" % (self.full_name, self.designation)
