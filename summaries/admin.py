from django.contrib import admin

from .models import Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "text",
        "publications_number",
    ]

    @admin.display(description="publications")
    def publications_number(self, obj):
        return obj.publications.count()
