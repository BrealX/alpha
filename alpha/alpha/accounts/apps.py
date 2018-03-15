from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'accounts'


    def ready(self):
        import accounts.signals
