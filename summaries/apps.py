from django.apps import AppConfig
from datetime import timedelta

from commons.tasks import RepeatTimer


class SummariesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summaries"

    def ready(self):
        self.start_background_task()

    def start_background_task(self):
        from .tasks import (
            create_summaries,
        )

        RepeatTimer(timedelta(hours=6), create_summaries).start()
