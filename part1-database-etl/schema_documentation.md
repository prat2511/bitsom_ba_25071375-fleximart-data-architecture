ENTITY: customers

Purpose:
Stores customer master information for FlexiMart.

Attributes:

- customer_id (PK): Unique surrogate identifier for each customer
- first_name: Customer’s first name
- last_name: Customer’s last name
- email: Unique email address of the customer
- phone: Customer contact number
- city: City where the customer is located
- registration_date: Date when the customer registered

Relationships:One customer can place many orders (1 : M relationship with orders table)
___________________________________________________________
ENTITY: products

Purpose:Stores product catalog information available for sale.

Attributes:

- product_id (PK): Unique surrogate identifier for each product
- product_name: Name of the product
- category: Product category (Electronics, Fashion, Groceries)
- price: Unit selling price of the product
- stock_quantity: Available stock count

Relationships:One product can appear in many order items(1 : M relationship with order_items table)
__________________________________________________________________________________________________________________
ENTITY: orders

Purpose:Stores order-level transaction information.

Attributes:

- order_id (PK): Unique surrogate identifier for each order
- customer_id (FK): References customers.customer_id
- order_date: Date when the order was placed
- total_amount: Total monetary value of the order
- status: Order status (Completed, Pending, Cancelled)

Relationships:Each order belongs to one customer.One order can contain many order items

__________________________________________________________________________________________________________

ENTITY: order_items

Purpose:Stores item-level details for each order.

Attributes:
- order_item_id (PK): Unique surrogate identifier for each order item
- order_id (FK): References orders.order_id
- product_id (FK): References products.product_id
- quantity: Number of units ordered
- unit_price: Price per unit at the time of order
- subtotal: Line item total (quantity × unit_price)

Relationships:Each order item belongs to one order.Each order item references one product
______________
2. Normalization Explanation : Data ensure integrity and eliminate redundancy.


3NF Compliance
 First Normal Form (1NF):
- All tables contain atomic values with no repeating groups.

Second Normal Form (2NF):
- There are no partial dependencies because all tables use single-column primary keys.

Third Normal Form (3NF):
- There are no transitive dependencies. Non-key attributes do not depend on other non-key attributes.

This design ensures consistency, scalability, and efficient data management.

Functional Dependencies
- In customers, all non-key attributes (first_name, last_name, email, phone, city, registration_date) depend only on customer_id.
- In products, all non-key attributes depend only on product_id.
- In orders, attributes such as order_date, total_amount, and status depend only on order_id.
- In order_items, quantity, unit_price, and subtotal depend only on order_item_id.



Anomaly Prevention

- Insert Anomalies:New customers or products can be added without requiring an order.
- Update Anomalies:Customer or product details are stored once and updated in a single place.
- Delete Anomalies:Deleting an order does not remove customer or product master data.

customers

| customer_id | first_name | last_name | email                                                   | phone          | city      | registration_date |
| ----------- | ---------- | --------- | ------------------------------------------------------- | -------------- | --------- | ----------------- |
|           1 | Rahul      | Sharma    | [rahul.sharma@gmail.com](mailto:rahul.sharma@gmail.com) | +91-9876543210 | Bangalore | 2023-01-15        |
|           2 | Priya      | Patel     | [priya.patel@yahoo.com](mailto:priya.patel@yahoo.com)   | +91-9988776655 | Mumbai    | 2023-02-20        |


products
| product_id | product_name       | category    | price    | stock_quantity |
| ---------- | ------------------ | ----------- | -------- | -------------- |
|          1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150            |
|          2 | Nike Running Shoes | Fashion     | 3499.00  | 80             |

orders 
| order_id | customer_id | order_date | total_amount | status    |
| -------- | ----------: | ---------- | ------------ | --------- |
|        1 |           1 | 2024-01-15 | 45999.00     | Completed |
|        2 |           2 | 2024-01-16 | 5998.00      | Completed |


order_items : 
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
| ------------- | -------: | ---------: | -------: | ---------: | -------: |
|             1 |        1 |          1 |        1 |   45999.00 | 45999.00 |
|             2 |        2 |          2 |        2 |    2999.00 |  5998.00 |

