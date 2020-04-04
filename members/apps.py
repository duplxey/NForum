from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        super().ready()

        # This is required in order to register the signals
        from . import signals
