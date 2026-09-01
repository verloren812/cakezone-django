"""Main URL configuration of the cakezone project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),            # home page
    path("menu/", include("menu.urls")),       # menu and pricing
    path("team/", include("team.urls")),       # master chefs
    path("service/", include("service.urls")), # services
    path("contact/", include("contact.urls")), # contacts
]

# in debug mode Django itself serves the media files (chef and dish photos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# admin site headers
admin.site.site_header = "CakeZone - control panel"
admin.site.site_title = "CakeZone"
admin.site.index_title = "Site content management"
