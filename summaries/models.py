from django.db import models

from publications.models import Publication


class Summary(models.Model):
    class Meta:
        verbose_name_plural = "summaries"

    text = models.TextField()
    publications = models.ManyToManyField(Publication, related_name="summaries")

    def __str__(self):
        return f"Summary({self.id})"
