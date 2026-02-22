from typing import Optional, List
from elasticsearch import Elasticsearch
from app.models.resume import Resume

RESUME_INDEX = "resumes"


class ResumeSearchService:
    """
    Elasticsearch indexing & search for resumes.
    PostgreSQL remains the source of truth.
    """

    @staticmethod
    def create_index(es: Elasticsearch) -> None:
        if es.indices.exists(index=RESUME_INDEX):
            return

        es.indices.create(
            index=RESUME_INDEX,
            mappings={
                "properties": {
                    "filename": {"type": "keyword"},
                    "content": {"type": "text"},
                    "skills": {"type": "keyword"},
                    "experience_years": {"type": "float"},
                }
            },
        )

    @staticmethod
    def index_resume(es: Elasticsearch, resume: Resume) -> None:
        es.index(
            index=RESUME_INDEX,
            id=resume.id,
            document={
                "filename": resume.filename,
                "content": resume.content,
                "skills": resume.skills,
                "experience_years": resume.experience_years,
            },
        )

    @staticmethod
    def search(
        es: Elasticsearch,
        query: Optional[str] = None,
        skills: Optional[List[str]] = None,
        min_experience: Optional[float] = None,
    ):
        must = []
        filters = []

        if query:
            must.append(
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["content", "skills"],
                    }
                }
            )

        if skills:
            filters.append({"terms": {"skills": skills}})

        if min_experience is not None:
            filters.append(
                {"range": {"experience_years": {"gte": min_experience}}}
            )

        es_query = {
            "query": {
                "bool": {
                    "must": must if must else {"match_all": {}},
                    "filter": filters,
                }
            }
        }

        response = es.search(index=RESUME_INDEX, body=es_query)

        return [
            {
                "resume_id": hit["_id"],
                "score": hit["_score"],
                "source": hit["_source"],
            }
            for hit in response["hits"]["hits"]
        ]
