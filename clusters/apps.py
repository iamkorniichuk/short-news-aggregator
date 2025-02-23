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
            create_clusters,
            populate_digests,
        )

        RepeatTimer(timedelta(days=1), create_clusters).start()
        RepeatTimer(timedelta(minutes=1), populate_digests).start()
