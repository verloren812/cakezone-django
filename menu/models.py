from django.db import models


class Category(models.Model):
    """A dish category (the Birthday / Wedding / Custom tabs on the menu page)."""

    name = models.CharField("name", max_length=100)
    slug = models.SlugField("URL slug", max_length=100, unique=True)
    description = models.CharField("description", max_length=300, blank=True)
    order = models.PositiveSmallIntegerField("display order", default=0)
    is_active = models.BooleanField("show on the site", default=True)

    class Meta:
        verbose_name = "dish category"
        verbose_name_plural = "dish categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    """A dish (a cake) in the menu."""

    category = models.ForeignKey(
        Category,
        verbose_name="category",
        on_delete=models.CASCADE,
        related_name="dishes",
    )
    name = models.CharField("name", max_length=150)
    description = models.TextField("description", blank=True)
    price = models.DecimalField("price", max_digits=8, decimal_places=2)
    weight = models.PositiveIntegerField("weight, g", null=True, blank=True)
    image = models.ImageField("photo", upload_to="dishes/", blank=True)
    is_active = models.BooleanField("in stock", default=True)
    created_at = models.DateTimeField("created at", auto_now_add=True)

    class Meta:
        verbose_name = "dish"
        verbose_name_plural = "dishes"
        ordering = ["category", "name"]

    def __str__(self):
        return "%s (%s)" % (self.name, self.category.name)
