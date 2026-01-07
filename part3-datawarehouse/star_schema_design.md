# Star Schema Design – FlexiMart Data Warehouse

## Section 1: Schema Overview

### FACT TABLE: fact_sales
**Grain:** One row per product per order line item  
**Business Process:** Sales transactions

**Measures (Numeric Facts):**
- quantity_sold: Number of units sold in a transaction
- unit_price: Price per unit at the time of sale
- discount_amount: Discount applied to the transaction line
- total_amount: Final sales value (quantity_sold × unit_price − discount_amount)

**Foreign Keys:**
- date_key → dim_date
- product_key → dim_product
- customer_key → dim_customer

---

### DIMENSION TABLE: dim_date
**Purpose:** Enables time-based analysis of sales  
**Type:** Conformed dimension

**Attributes:**
- date_key (PK): Surrogate key in YYYYMMDD format
- full_date: Actual calendar date
- day_of_week: Name of the day (Monday, Tuesday, etc.)
- day_of_month: Day number within the month
- month: Month number (1–12)
- month_name: Month name (January, February, etc.)
- quarter: Quarter of the year (Q1–Q4)
- year: Calendar year
- is_weekend: Indicates weekend or weekday

---

### DIMENSION TABLE: dim_product
**Purpose:** Stores product-related descriptive information

**Attributes:**
- product_key (PK): Surrogate key generated in data warehouse
- product_id: Business product identifier from source systems
- product_name: Name of the product
- category: Product category (Electronics, Fashion, Groceries)
- subcategory: Product subcategory
- unit_price: Standard price reference

---

### DIMENSION TABLE: dim_customer
**Purpose:** Stores customer attributes for segmentation and geography analysis

**Attributes:**
- customer_key (PK): Surrogate key generated in data warehouse
- customer_id: Business customer identifier from source systems
- customer_name: Full customer name
- city: Customer city
- state: Customer state
- customer_segment: Customer classification (Retail, Corporate, Premium)

---

## Section 2: Design Decisions

The fact table granularity is defined at the transaction line-item level, meaning each record represents the sale of one product within an order. This level of detail allows the data warehouse to support flexible analysis such as product-level performance, category roll-ups, customer behavior analysis, and time-based trends. Choosing a finer grain ensures that future analytical requirements can be supported without redesigning the schema.

Surrogate keys are used for all dimension tables instead of natural keys to improve performance and maintain consistency. Natural keys from source systems may change over time or vary across systems, while surrogate keys remain stable and numeric, making joins faster and easier to manage.

This star schema design supports drill-down and roll-up operations effectively. Analysts can roll up sales data by year, quarter, or month using the date dimension, and drill down to individual products or customers using the product and customer dimensions. The separation of facts and dimensions ensures clarity, scalability, and analytical efficiency.

---

## Section 3: Sample Data Flow

**Source Transaction:**  
Order #101, Customer "John Doe", Product "Laptop", Quantity: 2, Unit Price: 50000

**Data Warehouse Representation:**

**fact_sales**
- date_key: 20240115
- product_key: 5
- customer_key: 12
- quantity_sold: 2
- unit_price: 50000
- discount_amount: 0
- total_amount: 100000

**dim_date**
- date_key: 20240115
- full_date: 2024-01-15
- month: 1
- month_name: January
- quarter: Q1
- year: 2024
- is_weekend: FALSE

**dim_product**
- product_key: 5
- product_name: Laptop
- category: Electronics
- subcategory: Laptops

**dim_customer**
- customer_key: 12
- customer_name: John Doe
- city: Mumbai
- state: Maharashtra
- customer_segment: Retail
