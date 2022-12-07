from pystagram.settings.common import *

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "debug_toolbar",
] + THIRD_PARTY_APPS

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")

DATABASES = {
    "default": {
        "HOST": "",
        "PORT": "",
        "NAME": "pystagram",
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "ENGINE": "django.db.backends.mysql",
    }
}
