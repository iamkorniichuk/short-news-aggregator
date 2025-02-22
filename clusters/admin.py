from django.contrib import admin

from publications.models import Publication

from .models import Cluster


class MessageInline(admin.TabularInline):
    model = Publication


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "digest",
        "messages_number",
    ]
    inlines = [
        MessageInline,
    ]

    @admin.display(description="messages")
    def messages_number(self, obj):
        return obj.messages.count()
