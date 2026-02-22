from typing import Optional, List
from elasticsearch import Elasticsearch
from app.models.job import Job

JOB_INDEX = "jobs"


class JobSearchService:
    """
    Elasticsearch job indexing & search.
    PostgreSQL remains the source of truth.
    """

    @staticmethod
    def create_index(es: Elasticsearch) -> None:
        if es.indices.exists(index=JOB_INDEX):
            return
        # Use a mapping that keeps keywords for exact fields and text for full-text
        es.indices.create(
            index=JOB_INDEX,
            mappings={
                "properties": {
                    "title": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
                    "company": {"type": "keyword"},
                    "description": {"type": "text"},
                    "required_skills": {"type": "keyword"},
                    "location": {"type": "keyword"},
                    "salary": {"type": "keyword"},
                }
            },
        )

    @staticmethod
    def index_job(es: Elasticsearch, job: Job) -> None:
        es.index(
            index=JOB_INDEX,
            id=job.id,
            document={
                "title": job.title,
                "company": job.company,
                "description": job.description,
                # ensure required_skills indexes as array of keywords
                "required_skills": job.required_skills or [],
                "location": job.location,
                "owner_id": job.owner_id if hasattr(job, "owner_id") else None,
                "salary": job.salary,
            },
        )

    @staticmethod
    def delete_job(es: Elasticsearch, job_id: int) -> None:
        try:
            es.delete(index=JOB_INDEX, id=job_id)
        except Exception:
            # ignore missing docs
            pass

    @staticmethod
    def reindex_all(es: Elasticsearch, jobs: list[Job]) -> None:
        # recreate index mapping and bulk index
        if es.indices.exists(index=JOB_INDEX):
            es.indices.delete(index=JOB_INDEX)
        JobSearchService.create_index(es)
        from elasticsearch import helpers

        actions = []
        for job in jobs:
            actions.append({
                "_index": JOB_INDEX,
                "_id": job.id,
                "_source": {
                    "title": job.title,
                    "company": job.company,
                    "description": job.description,
                    "required_skills": job.required_skills or [],
                    "location": job.location,
                    "salary": job.salary,
                    "owner_id": job.owner_id if hasattr(job, "owner_id") else None,
                },
            })

        if actions:
            helpers.bulk(es, actions)

    @staticmethod
    def search(
        es: Elasticsearch,
        query: Optional[str] = None,
        location: Optional[str] = None,
        skills: Optional[List[str]] = None,
        page: int = 1,
        size: int = 10,
        sort_by: str = "relevance",
        order: str = "desc",
    ):
        # Build ES query with fuzziness, title boosting and skill filters
        must_clauses = []
        filter_clauses = []

        if query:
            must_clauses.append(
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title^3",
                            "description",
                            "company",
                        ],
                        "fuzziness": "AUTO",
                    }
                }
            )

        if skills:
            # require that at least one of the required_skills matches
            filter_clauses.append({"terms": {"required_skills": skills}})

        if location:
            filter_clauses.append({"term": {"location": location}})

        from_ = (page - 1) * size

        es_query = {
            "from": from_,
            "size": size,
            "query": {
                "bool": {
                    "must": must_clauses if must_clauses else [{"match_all": {}}],
                    "filter": filter_clauses,
                }
            },
        }

        # default: rely on ES relevance; allow explicit sorting by created_at or salary
        if sort_by != "relevance":
            es_query["sort"] = [{sort_by: {"order": order}}]

        response = es.search(index=JOB_INDEX, body=es_query)

        total = 0
        hits = []
        if response and "hits" in response:
            total = response["hits"]["total"]["value"] if isinstance(response["hits"]["total"], dict) else response["hits"]["total"]
            hits = response["hits"]["hits"]

        return {
            "page": page,
            "size": size,
            "total": total,
            "results": [
                {
                    "job_id": int(hit["_id"]),
                    "score": hit.get("_score"),
                    "source": hit.get("_source"),
                }
                for hit in hits
            ],
        }
