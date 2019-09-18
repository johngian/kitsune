from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'kitsune.users'
    label = 'users'

    def ready(self):
        from kitsune.users import signals  # noqa
