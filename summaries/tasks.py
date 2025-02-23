import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
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
        obj.publications.set(ids)
        obj.save()


def clusterize_queryset(queryset):
    values = list(queryset.values())
    dataframe = pd.DataFrame(values)

    scaler = StandardScaler()
    matrix = np.vstack(dataframe.embedding.values)
    scaled_matrix = scaler.fit_transform(matrix)

    hdbscan = HDBSCAN(
        min_cluster_size=3,
        algorithm="kdtree",
        cluster_selection_method="leaf",
    )
    hdbscan.fit(scaled_matrix)

    dataframe["cluster"] = hdbscan.labels_

    return dataframe.groupby("cluster")
