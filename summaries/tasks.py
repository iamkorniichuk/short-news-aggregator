from transformers import pipeline
import numpy as np
import pandas as pd
from sklearn.cluster._hdbscan.hdbscan import HDBSCAN

from summaries.models import Summary
from publications.models import Publication


summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)


def create_summaries():
    left_publications = (
        Publication.objects.filter(
            summaries=None,
        )
        .order_by("-views")
        .all()
    )
    dataframe, noise = clusterize_publications(left_publications)

    for pk in noise["id"].tolist():
        obj = Publication.objects.get(pk=pk)
        obj.delete()

    for _, publications in dataframe:
        length = min(len(publications), 20)
        ids = publications["id"].tolist()[:length]
        texts = publications["text"].tolist()[:length]

        text = "\n".join(texts)

        response = summarizer(
            text,
            max_length=200,
            min_length=20,
            do_sample=False,
        )
        summary = Summary(text=response[0]["summary_text"])
        summary.save()
        summary.publications.set(ids)
        summary.save()


def clusterize_publications(queryset):
    values = list(queryset.values("id", "embedding", "text"))
    dataframe = pd.DataFrame(values)

    if dataframe.empty:
        return {}

    matrix = np.vstack(dataframe.embedding.values)

    hdbscan = HDBSCAN(
        min_cluster_size=5,
        metric="euclidean",
        cluster_selection_method="eom",
    )
    labels = hdbscan.fit_predict(matrix)

    dataframe["cluster"] = labels
    noise = dataframe[dataframe["cluster"] == -1]
    dataframe = dataframe[dataframe["cluster"] != -1]

    return dataframe.groupby("cluster"), noise
