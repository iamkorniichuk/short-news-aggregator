from django.db import models

from commons.models import EmbeddingField
from channels.models import Channel
from clusters.models import Cluster


class Publication(models.Model):
    class Meta:
        unique_together = [["telegram_id", "channel"]]

    text = models.TextField()
    datetime = models.DateTimeField()
    telegram_id = models.PositiveIntegerField()
    channel = models.ForeignKey(
        Channel,
        models.RESTRICT,
        related_name="publications",
    )
    embedding = EmbeddingField(blank=True, null=True)
    cluster = models.ForeignKey(
        Cluster,
        models.SET_NULL,
        related_name="publications",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return f"https://www.t.me/{self.channel.username}/{self.telegram_id}"

    def __str__(self):
        return f"Publication({self.pk})"
