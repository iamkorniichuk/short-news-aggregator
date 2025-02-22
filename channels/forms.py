from django import forms
from django.conf import settings

from telethon.client import TelegramClient
from asgiref.sync import async_to_sync

from .models import Channel


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ["username"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.channel_id = self.get_channel_id(instance.username)
        if commit:
            instance.save()
        return instance

    @async_to_sync
    async def get_channel_id(self, username):
        async with TelegramClient(
            "Gathering channels' info",
            settings.TELETHON["API_ID"],
            settings.TELETHON["API_HASH"],
        ) as client:
            entity = await client.get_entity(username)
            return entity.id
