from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, unique=True, nullable=False)
    
    # Relationship with Employee
    employees = relationship("Employee", back_populates="department")
    
    def __repr__(self):
        return f"Department(id={self.id}, department={self.department})"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, unique=True, nullable=False)
    
    # Relationship with Employee
    employees = relationship("Employee", back_populates="job")
    
    def __repr__(self):
        return f"Job(id={self.id}, job={self.job})"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(String, nullable=False)  # ISO format string
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    # Relationships
    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
    
    def __repr__(self):
        return f"Employee(id={self.id}, name={self.name}, department_id={self.department_id}, job_id={self.job_id})"
