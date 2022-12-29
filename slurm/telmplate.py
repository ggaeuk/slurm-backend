from pydantic import BaseModel


class Job(BaseModel):
    jobs: dict