from django.contrib import admin

from commons.admin import ExternalLinkTag

from .models import Channel
from .forms import ChannelForm


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username_with_url",
        "telegram_id",
        "publications_number",
    ]
    form = ChannelForm

    username_with_url = admin.display(
        ExternalLinkTag(
            href="get_absolute_url",
            alt="username",
            inner_text="username",
            open_new_tab=True,
        ),
        description="username",
    )

    @admin.display(description="publications")
    def publications_number(self, obj):
        return obj.publications.count()
