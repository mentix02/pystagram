from django.apps import AppConfig


class UserConfig(AppConfig):

    name = "user"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from user.signals import create_auth_token  # noqa
