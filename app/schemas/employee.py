from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    datetime: str
    department_id: int
    job_id: int

    @validator('datetime')
    def validate_datetime(cls, v):
        try:
            # Validate ISO format
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Datetime must be in ISO format')

class EmployeeCreate(EmployeeBase):
    id: int

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
