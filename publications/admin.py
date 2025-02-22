from django.contrib import admin

from commons.admin import ExternalLinkTag, bool_filter_factory

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "datetime",
        "message_url",
        "is_embedded",
    ]
    list_filter = [
        bool_filter_factory(
            "embedding",
            title="is embedding null",
            filter_lookup="isnull",
        )
    ]
    message_url = admin.display(
        ExternalLinkTag(
            href="get_absolute_url",
            alt="__str__",
            inner_text="get_absolute_url",
            open_new_tab=True,
        ),
        description="message",
    )

    @admin.display(description="is embedded")
    def is_embedded(self, obj):
        return obj.embedding is not None
