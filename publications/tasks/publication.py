from django.conf import settings

from telethon.client import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from emoji import replace_emoji
import re

from publications.models import Publication
from channels.models import Channel


async def gather_publications():
    async with TelegramClient(
        "Gathering messages",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        async for channel in Channel.objects.all():
            recent_message = await channel.messages.order_by("-datetime").afirst()
            message_id = recent_message.message_id if recent_message else 0
            telegram_messages = await get_new_messages(
                client,
                channel.username,
                message_id,
            )
            await save_telegram_messages(telegram_messages.messages)


async def save_telegram_messages(messages):
    result = await Publication.objects.abulk_create(
        [
            Publication(
                message_id=obj.id,
                channel=await Channel.objects.aget(channel_id=obj.peer_id.channel_id),
                text=clear_text(obj.message),
                datetime=obj.date,
            )
            for obj in messages
            if obj.message
        ]
    )
    return result


def clear_text(text):
    text = replace_emoji(text, "")

    text = re.sub(r"http\S+|www\S+", "", text)

    text = text.replace("\n", " ").replace("\r", "")

    return text


async def get_new_messages(client, username, recent_message_id):
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
            min_id=recent_message_id,
            **optional_kwargs,
        )
    )
    return messages
