from django.conf import settings

import re
import emoji
from telethon.client import TelegramClient
from telethon.tl.functions.messages import GetMessagesViewsRequest
from sentence_transformers import SentenceTransformer


from publications.models import Publication
from channels.models import Channel


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


async def gather_publications():
    async with TelegramClient(
        "publications",
        settings.TELETHON["API_ID"],
        settings.TELETHON["API_HASH"],
    ) as client:
        client.parse_mode = "md"
        async for channel in Channel.objects.all():
            recent_publication = await channel.publications.order_by(
                "-datetime"
            ).afirst()

            telegram_id = recent_publication.telegram_id if recent_publication else 0
            peer = await client.get_entity(channel.username)

            telegram_publications = await get_new_publications(
                client,
                peer,
                telegram_id,
            )
            publication_ids = [obj.id for obj in telegram_publications]

            response = await client(
                GetMessagesViewsRequest(
                    peer=peer,
                    id=publication_ids,
                    increment=False,
                )
            )
            await save_telegram_publications(telegram_publications, response.views)


async def save_telegram_publications(publications, views_list):
    results = []
    for i, obj in enumerate(publications):
        if not obj.text:
            continue

        text = clean_text(obj.text)

        channel = await Channel.objects.aget(telegram_id=obj.peer_id.channel_id)
        embedding = get_embedding(text)

        results.append(
            Publication(
                telegram_id=obj.id,
                channel=channel,
                text=text,
                embedding=embedding,
                datetime=obj.date,
                views=views_list[i].views,
            )
        )

    await Publication.objects.abulk_create(results)
    return results


def get_embedding(text):
    return embedding_model.encode(text, normalize_embeddings=True).tolist()


def clean_text(text):
    # Remove markdown formatting
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
    text = re.sub(r"~~(.*?)~~", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)

    # Remove hashtags
    text = re.sub(r"#\w+", "", text)

    # Remove emojis
    text = emoji.replace_emoji(text, "")

    # Remove leading and trailing URLs (both markdown and plain URL)
    url_pattern = r"(https?://\S+|\[.*?\]\(https?://\S+\))"
    while re.match(rf"^\s*{url_pattern}(\s+{url_pattern})*\s*", text):
        text = re.sub(rf"^\s*{url_pattern}(\s+{url_pattern})*\s*", "", text)

    while re.search(rf"\s*{url_pattern}(\s+{url_pattern})*\s*$", text):
        text = re.sub(rf"\s*{url_pattern}(\s+{url_pattern})*\s*$", "", text)

    # Remove all URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove markdown links, preserving only the label
    def replace_markdown_links(m):
        label = m.group(1)
        label = re.sub(r"[\[\]\(\)]", "", label).strip()
        return label

    text = re.sub(r"\[(.*?)\]\(https?://\S+\)", replace_markdown_links, text)

    # Remove handlers
    text = re.sub(r"^@\w+\s*", "", text)
    text = re.sub(r"\s*@\w+$", "", text)

    # Remove extra whitespace
    text = text.strip()

    return text


async def get_new_publications(client, peer, recent_publication_id):
    messages = await client.get_messages(
        peer,
        limit=20,
        min_id=recent_publication_id,
    )
    return messages
