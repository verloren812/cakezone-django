"""Production settings: debug is off, the key and the hosts must come from the environment."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import ALLOWED_HOSTS, SECRET_KEY, env_bool

DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY environment variable is not set.")

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS environment variable is not set "
        "(comma separated list, e.g. cakezone.example.com,www.cakezone.example.com)."
    )

# HTTPS: can be disabled with DJANGO_SECURE_SSL=false, e.g. for a local check of prod settings
SECURE_SSL = env_bool("DJANGO_SECURE_SSL", default=True)

SECURE_SSL_REDIRECT = SECURE_SSL
SESSION_COOKIE_SECURE = SECURE_SSL
CSRF_COOKIE_SECURE = SECURE_SSL
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30 if SECURE_SSL else 0  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_SSL
# when the site runs behind a reverse proxy (nginx) that terminates HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
