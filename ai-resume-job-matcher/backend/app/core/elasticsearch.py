from elasticsearch import Elasticsearch, exceptions as es_exceptions
from app.core.config import settings
import logging


def get_es_client() -> Elasticsearch:
    """Create an Elasticsearch client and verify connectivity.

    This is lightweight and will raise a clear exception if ES isn't reachable.
    """
    url = settings.ELASTICSEARCH_URL
    # allow passing a single url or comma separated
    hosts = [h.strip() for h in url.split(",")] if "," in url else [url]

    client = Elasticsearch(hosts)

    try:
        if not client.ping():
            logging.warning("Elasticsearch ping failed for hosts=%s", hosts)
    except es_exceptions.ElasticsearchException as e:
        logging.exception("Elasticsearch client could not connect: %s", e)

    return client
