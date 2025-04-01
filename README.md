DB Migration REST API
A Python-based REST API for migrating data from CSV files to a SQL database. This API supports batch transactions and handles three data tables: departments, jobs, and employees.

Project Overview
This REST API is designed to facilitate database migration by:

Receiving historical data from CSV files
Processing and validating the data
Uploading the data to a new SQL database
Supporting batch transactions (1 up to 1000 rows) with a single request

Database Models

- Department
  id (INTEGER): Department ID
  department (STRING): Department name

- Job
  id (INTEGER): Job ID
  job (STRING): Job title

- Employee
  id (INTEGER): Employee ID
  name (STRING): Employee name
  datetime (STRING): Hire datetime in ISO format
  department_id (INTEGER): Foreign key to department
  job_id (INTEGER): Foreign key to job
