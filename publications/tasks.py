from django.conf import settings

from telethon.client import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from sentence_transformers import SentenceTransformer
from emoji import replace_emoji
import re

from publications.models import Publication
from channels.models import Channel


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


async def gather_publications():
    async with TelegramClient(
        "publications",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        async for channel in Channel.objects.all():
            recent_publication = await channel.publications.order_by(
                "-datetime"
            ).afirst()
            telegram_id = recent_publication.telegram_id if recent_publication else 0
            telegram_publications = await get_new_publications(
                client,
                channel.username,
                telegram_id,
            )
            await save_telegram_publications(telegram_publications.messages)


async def save_telegram_publications(publications):
    results = []
    for obj in publications:
        if not obj.message:
            continue

        text = clear_text(obj.message)
        channel = await Channel.objects.aget(telegram_id=obj.peer_id.channel_id)
        embedding = get_embedding(text)
        results.append(
            Publication(
                telegram_id=obj.id,
                channel=channel,
                text=text,
                embedding=embedding,
                datetime=obj.date,
            )
        )

    await Publication.objects.abulk_create(results)
    return results


def get_embedding(text):
    return embedding_model.encode(text).tolist()


def clear_text(text):
    text = replace_emoji(text, "")

    text = re.sub(r"http\S+|www\S+", "", text)

    text = text.replace("\n", " ").replace("\r", "")

    return text


async def get_new_publications(client, username, recent_publication_id):
    channel = await client.get_entity(username)
    optional_kwargs = {
        "offset_id": 0,
        "offset_date": None,
        "add_offset": 0,
        "max_id": 0,
        "hash": 0,
    }
    messages = await client(
        GetHistoryRequest(
            peer=channel,
            limit=100,
            min_id=recent_publication_id,
            **optional_kwargs,
        )
    )
    return messages
