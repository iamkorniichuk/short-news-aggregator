from openai.embeddings_utils import get_embedding
from openai.error import RateLimitError
from tenacity import RetryError

from publications.models import Publication


def populate_embedding():
    left_publications = (
        Publication.objects.filter(embedding__isnull=True).order_by("datetime").all()
    )
    for publication in left_publications:
        try:
            publication.embedding = get_embedding(
                publication.text, "text-embedding-ada-002"
            )
            publication.save()
        except (RateLimitError, RetryError) as error:
            print("Embedding's rate limit is exceeded.", error)
            break
