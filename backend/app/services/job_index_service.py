from elasticsearch import Elasticsearch
from app.models.job import Job

INDEX_NAME = "jobs"


class JobIndexService:
    @staticmethod
    def index_job(es: Elasticsearch, job: Job) -> None:
        document = {
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "required_skills": job.required_skills,
            "location": job.location,
            "salary": job.salary,
        }

        es.index(
            index=INDEX_NAME,
            id=job.id,
            document=document,
        )
