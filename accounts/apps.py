from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        super().ready()

        # This is required in order to register the signals
        from . import signals
