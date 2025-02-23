import numpy as np
import pandas as pd
from sklearn.cluster._hdbscan.hdbscan import HDBSCAN
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

from summaries.models import Summary
from publications.models import Publication


summarizer = TextRankSummarizer()


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
        parser = PlaintextParser.from_string(text, Tokenizer("english"))

        summary = summarizer(parser.document, 2)
        summary = " ".join(str(sentence) for sentence in summary)

        obj = Summary(text=summary)
        obj.save()
        obj.publications.set(ids)
        obj.save()


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
