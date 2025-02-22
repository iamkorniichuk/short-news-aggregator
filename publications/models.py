from django.db import models

from commons.models import EmbeddingField
from channels.models import Channel
from clusters.models import Cluster


class Publication(models.Model):
    class Meta:
        unique_together = [["message_id", "channel"]]

    text = models.TextField()
    datetime = models.DateTimeField()
    message_id = models.PositiveIntegerField()
    channel = models.ForeignKey(
        Channel,
        models.RESTRICT,
        related_name="messages",
    )
    embedding = EmbeddingField(blank=True, null=True)
    cluster = models.ForeignKey(
        Cluster,
        models.SET_NULL,
        related_name="messages",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return f"https://www.t.me/{self.channel.username}/{self.message_id}"

    def __str__(self):
        return f"Message({self.pk})"
