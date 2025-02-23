from django.contrib import admin

from commons.admin import ExternalLinkTag, bool_filter_factory

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "datetime",
        "publication_url",
    ]
    list_filter = [
        bool_filter_factory(
            "embedding",
            title="is embedding null",
            filter_lookup="isnull",
        )
    ]
    publication_url = admin.display(
        ExternalLinkTag(
            href="get_absolute_url",
            alt="__str__",
            inner_text="get_absolute_url",
            open_new_tab=True,
        ),
        description="publication",
    )
