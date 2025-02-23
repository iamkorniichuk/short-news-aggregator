from django.contrib import admin

from commons.admin import ExternalLinkTag

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "datetime",
        "publication_url",
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
