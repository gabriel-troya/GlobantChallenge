from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any, Type, TypeVar, Generic, Optional
from app.database.models import Department, Job, Employee
from app.schemas.department import DepartmentCreate
from app.schemas.job import JobCreate
from app.schemas.employee import EmployeeCreate
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')
CreateSchemaType = TypeVar('CreateSchemaType')

class DBService(Generic[T, CreateSchemaType]):
    """Generic database service for CRUD operations"""
    
    def __init__(self, model: Type[T]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[T]:
        """Get a single record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Get multiple records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> T:
        """Create a single record"""
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_batch(self, db: Session, *, objs_in: List[CreateSchemaType]) -> List[T]:
        """Create multiple records in a batch"""
        db_objs = [self.model(**obj_in.model_dump()) for obj_in in objs_in]
        db.add_all(db_objs)
        db.commit()
        for obj in db_objs:
            db.refresh(obj)
        return db_objs
    
    def create_or_update_batch(self, db: Session, *, objs_in: List[CreateSchemaType]) -> List[T]:
        """Create or update multiple records in a batch"""
        results = []
        
        for obj_in in objs_in:
            # Check if record exists
            db_obj = self.get(db, id=obj_in.id)
            
            if db_obj:
                # Update existing record
                obj_data = obj_in.model_dump()
                for key, value in obj_data.items():
                    setattr(db_obj, key, value)
                results.append(db_obj)
            else:
                # Create new record
                db_obj = self.model(**obj_in.model_dump())
                db.add(db_obj)
                results.append(db_obj)
        
        db.commit()
        for obj in results:
            db.refresh(obj)
        
        return results

    def delete(self, db: Session, *, id: int) -> T:
        """Delete a record by ID"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


# Create service instances for each model
department_service = DBService[Department, DepartmentCreate](Department)
job_service = DBService[Job, JobCreate](Job)
employee_service = DBService[Employee, EmployeeCreate](Employee)
