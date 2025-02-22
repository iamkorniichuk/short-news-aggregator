from commons.data_processing import queryset_to_data_frame, clusterize

from clusters.models import Cluster
from publications.models import Publication


def create_clusters():
    grouped_df = get_messages_clusters()
    for id, messages in grouped_df:
        cluster = Cluster.objects.create()
        messages_id = messages["id"].tolist()
        for id in messages_id:
            message = Publication.objects.get(id=id)
            message.cluster = cluster
            message.save()


def get_messages_clusters():
    messages = get_unclestered_messages()
    df = queryset_to_data_frame(messages)
    clusters = clusterize(df)

    return clusters.groupby("cluster")


def get_unclestered_messages():
    return (
        Publication.objects.filter(
            embedding__isnull=False,
            cluster__isnull=True,
        )
        .order_by("datetime")
        .all()
    )
