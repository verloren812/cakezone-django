from django.db import models


class Establishment(models.Model):
    """Information about the establishment (the About block and the counters)."""

    name = models.CharField("name", max_length=100, default="CakeZone")
    slogan = models.CharField("slogan", max_length=200, blank=True)
    short_description = models.CharField("short description", max_length=300, blank=True)
    description = models.TextField("description", blank=True)
    image = models.ImageField("photo", upload_to="establishment/", blank=True)

    years_of_experience = models.PositiveIntegerField("years of experience", default=0)
    cakes_baked = models.PositiveIntegerField("cakes baked", default=0)
    happy_clients = models.PositiveIntegerField("happy clients", default=0)
    master_chefs = models.PositiveIntegerField("master chefs", default=0)
    awards = models.PositiveIntegerField("awards", default=0)

    is_active = models.BooleanField("show on the site", default=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    class Meta:
        verbose_name = "establishment"
        verbose_name_plural = "establishment"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """A client testimonial (the testimonial carousel on the home page)."""

    author_name = models.CharField("client name", max_length=100)
    profession = models.CharField("profession", max_length=100, blank=True)
    text = models.TextField("testimonial text")
    photo = models.ImageField("client photo", upload_to="testimonials/", blank=True)
    rating = models.PositiveSmallIntegerField("rating", default=5)
    is_published = models.BooleanField("published", default=True)
    created_at = models.DateTimeField("created at", auto_now_add=True)

    class Meta:
        verbose_name = "testimonial"
        verbose_name_plural = "testimonials"
        ordering = ["-created_at"]

    def __str__(self):
        return "Testimonial from " + self.author_name
