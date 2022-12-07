from decouple import config

CI = "ci"
PRODUCTION = "prod"
DEVELOPMENT = "dev"

ENVIRONMENT = config("ENVIRONMENT", default="dev")

if ENVIRONMENT == DEVELOPMENT:
    from pystagram.settings.dev import *
elif ENVIRONMENT == PRODUCTION:
    from pystagram.settings.prod import *
elif ENVIRONMENT == CI:
    from pystagram.settings.ci import *
else:
    raise ValueError("please configure environment value")


INSTALLED_APPS = (
    DEFAULT_APPS
    + THIRD_PARTY_APPS
    + LOCAL_APPS
    + [
        "django_cleanup",  # important to keep this at the end
    ]
)
