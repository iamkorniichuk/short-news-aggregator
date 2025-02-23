import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster._hdbscan.hdbscan import HDBSCAN
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

from clusters.models import Cluster
from publications.models import Publication


summarizer = TextRankSummarizer()


def create_clusters():
    left_publications = (
        Publication.objects.filter(
            cluster__isnull=True,
        )
        .order_by("datetime")
        .all()
    )
    dataframe = clusterize_queryset(left_publications)
    for id, publications in dataframe:
        cluster = Cluster.objects.create()
        publications_id = publications["id"].tolist()
        for id in publications_id:
            publication = Publication.objects.get(id=id)
            publication.cluster = cluster
            publication.save()

    populate_digests()


def populate_digests():
    left_clusters = Cluster.objects.exclude(digest__gt=0).all()
    for cluster in left_clusters:
        values = [publication.text for publication in cluster.publications]
        text = "\n".join(values)

        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = summarizer(parser.document, 2)

        digest = " ".join(str(sentence) for sentence in summary)
        cluster.digest = digest
        cluster.save()


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
