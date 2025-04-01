from typing import List, Optional
from pydantic import BaseModel

class DepartmentBase(BaseModel):
    department: str

class DepartmentCreate(DepartmentBase):
    id: int

class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
