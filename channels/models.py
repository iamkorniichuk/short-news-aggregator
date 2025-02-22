from django.db import models


class Channel(models.Model):
    username = models.CharField(max_length=32)
    channel_id = models.PositiveIntegerField()

    def get_absolute_url(self):
        return f"https://www.t.me/{self.username}"

    def __str__(self):
        return f"Channel({self.username})"
