import os
import shutil
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Union, Optional, Tuple
from app.config import settings
from app.schemas.department import DepartmentCreate
from app.schemas.job import JobCreate
from app.schemas.employee import EmployeeCreate
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CSVService:
    """Service for handling CSV file operations and validation"""
    
    @staticmethod
    def validate_csv_headers(file_path: Path, expected_headers: List[str]) -> bool:
        """Validate if CSV headers match expected headers"""
        try:
            df = pd.read_csv(file_path, nrows=0, sep=settings.CSV_DELIMITER)
            headers = df.columns.tolist()
            return set(headers) == set(expected_headers)
        except Exception as e:
            logger.error(f"Error validating CSV headers: {e}")
            return False
    
    @staticmethod
    def read_csv_to_dataframe(file_path: Path) -> pd.DataFrame:
        """Read CSV file into a pandas DataFrame"""
        return pd.read_csv(file_path, sep=settings.CSV_DELIMITER)
    
    @staticmethod
    def process_departments_csv(file_path: Path) -> List[DepartmentCreate]:
        """Process departments CSV file and return list of department schemas"""
        df = CSVService.read_csv_to_dataframe(file_path)
        
        # Validate required columns
        required_columns = ['ID', 'DEPARTMENT']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns in departments CSV: {missing}")
        
        # Process data
        departments = []
        for _, row in df.iterrows():
            department = DepartmentCreate(
                id=int(row['ID']),
                department=row['DEPARTMENT']
            )
            departments.append(department)
        
        return departments
    
    @staticmethod
    def process_jobs_csv(file_path: Path) -> List[JobCreate]:
        """Process jobs CSV file and return list of job schemas"""
        df = CSVService.read_csv_to_dataframe(file_path)
        
        # Validate required columns
        required_columns = ['ID', 'JOB']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns in jobs CSV: {missing}")
        
        # Process data
        jobs = []
        for _, row in df.iterrows():
            job = JobCreate(
                id=int(row['ID']),
                job=row['JOB']
            )
            jobs.append(job)
        
        return jobs
    
    @staticmethod
    def process_employees_csv(file_path: Path) -> List[EmployeeCreate]:
        """Process employees CSV file and return list of employee schemas"""
        df = CSVService.read_csv_to_dataframe(file_path)
        
        # Validate required columns
        required_columns = ['ID', 'NAME', 'DATETIME', 'DEPARTMENT_ID', 'JOB_ID']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns in employees CSV: {missing}")
        
        # Process data
        employees = []
        for _, row in df.iterrows():
            # Validate datetime format
            try:
                # Just verify it's ISO format, but keep as string
                datetime.fromisoformat(row['DATETIME'])
            except ValueError:
                logger.warning(f"Invalid datetime format for employee ID {row['ID']}: {row['DATETIME']}")
                continue
                
            employee = EmployeeCreate(
                id=int(row['ID']),
                name=row['NAME'],
                datetime=row['DATETIME'],
                department_id=int(row['DEPARTMENT_ID']),
                job_id=int(row['JOB_ID'])
            )
            employees.append(employee)
        
        return employees
    
    @staticmethod
    def batch_processor(items: List[Any], batch_size: int = settings.MAX_BATCH_SIZE) -> List[List[Any]]:
        """Split a list of items into batches of specified size"""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    
    @staticmethod
    def move_to_processed(file_path: Path) -> Path:
        """Move a processed file to the processed directory"""
        # Create timestamp to avoid overwriting files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = file_path.name
        new_filename = f"{filename.split('.')[0]}_{timestamp}.{filename.split('.')[-1]}"
        
        # Destination path
        dest_path = settings.CSV_PROCESSED_DIR / new_filename
        
        # Move file
        shutil.move(str(file_path), str(dest_path))
        
        return dest_path
