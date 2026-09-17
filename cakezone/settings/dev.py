"""Development settings: debug mode, local hosts only."""

import os

from django.core.management.utils import get_random_secret_key

from .base import *  # noqa: F401,F403
from .base import env_bool, env_list

DEBUG = env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]")

# No key is stored in the code. Without DJANGO_SECRET_KEY a random key is generated
# on every start: the project still runs right after cloning, but sessions (the admin
# login) are reset on restart. Put a key into .env to keep them.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or get_random_secret_key()
