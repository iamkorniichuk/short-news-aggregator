from django.apps import AppConfig
from datetime import timedelta

from commons.tasks import RepeatTimer


class PublicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "publications"

    def ready(self):
        self.start_background_task()

    def start_background_task(self):
        from .tasks import gather_publications

        RepeatTimer(timedelta(minutes=5), gather_publications, is_async=True).start()
