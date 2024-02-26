from django.apps import AppConfig


class ErpbackofficeConfig(AppConfig):
    name = 'ErpBackOffice'

    def ready(self):
        from ErpBackOffice import signals
