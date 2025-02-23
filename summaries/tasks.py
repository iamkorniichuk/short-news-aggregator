import numpy as np
import pandas as pd
from sklearn.cluster._hdbscan.hdbscan import HDBSCAN
from transformers import pipeline

from summaries.models import Summary
from publications.models import Publication


summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)


def create_summaries():
    left_publications = (
        Publication.objects.filter(
            summaries=None,
        )
        .order_by("datetime")
        .all()
    )
    dataframe = clusterize_queryset(left_publications)
    for _, publications in dataframe:
        ids = publications["id"].tolist()
        texts = publications["text"].tolist()

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


def clusterize_queryset(queryset):
    values = list(queryset.values("id", "embedding", "text"))
    dataframe = pd.DataFrame(values)

    if dataframe.empty:
        return {}

    matrix = np.vstack(dataframe.embedding.values)

    hdbscan = HDBSCAN(
        min_cluster_size=3,
        metric="euclidean",
        cluster_selection_method="leaf",
    )
    hdbscan.fit(matrix)

    dataframe["cluster"] = hdbscan.labels_

    return dataframe.groupby("cluster")
