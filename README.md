# FlexiMart Data Architecture Project

**Student Name:** Pratyush SINHA
**Student ID:** BITSoM_BA_25071375
**Email:** pratyush.sinha2511@gmail.com
**Date:** 07 January 2026

## Project Overview

This project implements an end-to-end data architecture solution for FlexiMart. 
It includes data ingestion and cleaning using Python, transactional storage using PostgreSQL, NoSQL analysis using MongoDB, and a star-schema-based data warehouse for analytical reporting. 
The project demonstrates ETL pipelines, relational and NoSQL database design, and OLAP analytics.


## Repository Structure
├── data/
│   ├── customers_raw.csv
│   ├── products_catalog.json
│   ├── products_raw.csv
│   └── sales_raw.csv	
│	
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   ├── data_quality_report.txt
│   ├── etl.log	
│   ├── Task1_dataQualityReport.png
│   ├── Task1_dataQualityReport_2.png
│   └── Task1.3_business_queries.png	
│  
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   ├── mongodb_operation_output.txt
│   ├── Task2_mongodb_operations1.png
│   ├── Task2_mongodb_operations2.png
│   ├── Task2_mongodb_operations3.png
│   └── Task2_mongodb_operations4.png
│
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   ├── analytics_queries.sql
│   └── query_output.png
└── README.md

## Technologies Used

-Python 3.14 – Core language for ETL pipeline implementation
-pandas 2.3.3 – Data cleaning, transformation, and validation
-SQLAlchemy 2.x – Database abstraction and bulk data loading
-psycopg2 – PostgreSQL driver for Python
-PostgreSQL 16.11 – Relational database for OLTP and data warehouse
-MongoDB 8.2.3 – NoSQL document database for product catalog
-mongosh 2.5.10 – MongoDB shell for executing queries and aggregations

## Setup Instructions

### Database Setup

```bash
# Create transactional and data warehouse databases
psql -U postgres -h localhost -c "CREATE DATABASE fleximart;"
psql -U postgres -h localhost -c "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
cd part1-database-etl
python etl_pipeline.py


# Run Part 1 - Business Queries
psql -U postgres -h localhost -d fleximart -f business_queries.sql

# Run Part 3 - Data Warehouse
cd part3-datawarehouse
psql -U postgres -h localhost -d fleximart_dw -f warehouse_schema.sql
psql -U postgres -h localhost -d fleximart_dw -f warehouse_data.sql
psql -U postgres -h localhost -d fleximart_dw -f analytics_queries.sql



### MongoDB Setup

cd part2-nosql
mongosh mongodb_operations.js


## Key Learnings
-Learned how to design and implement a complete ETL pipeline with data validation, logging, and error handling.
-Gained practical experience in relational modeling, normalization (3NF), and SQL analytics.
-Understood how MongoDB’s flexible document model supports complex and nested data structures.
-Implemented a star schema data warehouse and wrote OLAP queries for business analytics and reporting.

## Challenges Faced

1. Handling inconsistent data formats (dates, missing values)
-> Solved by implementing robust parsing logic, validation rules, and default handling strategies in the ETL pipeline.
2. Maintaining referential integrity during data loading
-> Solved by carefully sequencing inserts, using surrogate keys, and dropping invalid records that violated foreign key constraints.

