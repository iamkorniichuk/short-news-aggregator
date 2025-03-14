import uuid
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf import settings

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.manifold import TSNE
import os

from .models import Summary


PLOT_URL = os.path.join(settings.MEDIA_URL, "plots")
PLOT_DIR = os.path.join(settings.MEDIA_ROOT, "plots")


@admin.action(description="Plot selected clusters")
def plot(model_admin, request, queryset):
    dataframe = queryset_to_dataframe(queryset)
    matrix = np.vstack(dataframe["embedding"].values)
    path = plot_clusters(dataframe, matrix)

    url = f"{PLOT_URL}/{os.path.basename(path)}"
    return HttpResponseRedirect(url)


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "text",
        "publications_number",
    ]
    readonly_fields = ["publications_text"]
    actions = [plot]

    def publications_text(self, obj):
        result = ""
        for publication in obj.publications.all():
            pk = publication.pk
            text = publication.text
            result += f"{pk}: {text}\n\n"

        return result

    publications_text.short_description = "Publications text"

    @admin.display(description="publications")
    def publications_number(self, obj):
        return obj.publications.count()


def queryset_to_dataframe(queryset):
    data = []
    for summary in queryset:
        for publication in summary.publications.all():
            data.append(
                {
                    "cluster": summary.id,
                    "embedding": publication.embedding,
                }
            )

    return pd.DataFrame(data)


def plot_clusters(dataframe, matrix):
    tsne = TSNE(n_components=2, random_state=42)
    tsne_results = tsne.fit_transform(matrix)

    dataframe["tsne_x"] = tsne_results[:, 0]
    dataframe["tsne_y"] = tsne_results[:, 1]

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x="tsne_x",
        y="tsne_y",
        hue="cluster",
        data=dataframe,
        palette="viridis",
        legend="full",
        alpha=0.7,
    )
    plt.title("t-SNE visualization of HDBSCAN clusters")
    plt.xlabel("t-SNE Component 1")
    plt.ylabel("t-SNE Component 2")

    img_id = str(uuid.uuid4())
    plot_filename = f"plot_{img_id}.png"
    plot_path = os.path.join(PLOT_DIR, plot_filename)
    plt.savefig(plot_path)
    plt.close()

    return plot_path
