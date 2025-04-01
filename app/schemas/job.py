from typing import List, Optional
from pydantic import BaseModel

class JobBase(BaseModel):
    job: str

class JobCreate(JobBase):
    id: int

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
