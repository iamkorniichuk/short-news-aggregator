from django.conf import settings

from telethon.client import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from emoji import replace_emoji
import re

from publications.models import Publication
from channels.models import Channel


async def gather_publications():
    async with TelegramClient(
        "publications",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        async for channel in Channel.objects.all():
            recent_publication = await channel.messages.order_by("-datetime").afirst()
            telegram_id = recent_publication.telegram_id if recent_publication else 0
            telegram_publications = await get_new_publications(
                client,
                channel.username,
                telegram_id,
            )
            await save_telegram_publications(telegram_publications.messages)


async def save_telegram_publications(publications):
    result = await Publication.objects.abulk_create(
        [
            Publication(
                telegram_id=obj.id,
                channel=await Channel.objects.aget(telegram_id=obj.peer_id.channel_id),
                text=clear_text(obj.message),
                datetime=obj.date,
            )
            for obj in publications
            if obj.message
        ]
    )
    return result


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
