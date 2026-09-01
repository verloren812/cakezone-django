from django.urls import path, re_path

from . import views

app_name = "menu"

urlpatterns = [
    path("", views.index, name="index"),
    # a route built with a regular expression: /menu/cakes/, /menu/cup-cakes/ and so on
    re_path(r"^(?P<category>[a-z][a-z-]{2,20})/$", views.category, name="category"),
]
