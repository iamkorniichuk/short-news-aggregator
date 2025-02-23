from django.db.models.signals import pre_save
from django.dispatch import receiver

from sentence_transformers import SentenceTransformer

from .models import Publication


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


@receiver(pre_save, sender=Publication)
def set_embedding(sender, instance, *args, **kwargs):
    if instance._sate.adding:
        instance.embedding = embedding_model.encode(instance.text).tolist()
