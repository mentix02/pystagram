from pystagram.settings.common import *

DEBUG = True

# use SQLite for CI testing

DATABASES = {
    "default": {
        "NAME": BASE_DIR / "db.sqlite3",
        "ENGINE": "django.db.backends.sqlite3",
    }
}

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
