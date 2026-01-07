-- Database: fleximart_dw
-- Seed data for star schema (meets minimum data requirements)

BEGIN;

-- ----------------------------
-- dim_date (30 dates: Jan-Feb 2024)
-- ----------------------------
INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240120, '2024-01-20', 'Saturday', 20, 1, 'January',  'Q1', 2024, TRUE),
(20240121, '2024-01-21', 'Sunday',   21, 1, 'January',  'Q1', 2024, TRUE),
(20240122, '2024-01-22', 'Monday',   22, 1, 'January',  'Q1', 2024, FALSE),
(20240123, '2024-01-23', 'Tuesday',  23, 1, 'January',  'Q1', 2024, FALSE),
(20240124, '2024-01-24', 'Wednesday',24, 1, 'January',  'Q1', 2024, FALSE),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January',  'Q1', 2024, FALSE),
(20240126, '2024-01-26', 'Friday',   26, 1, 'January',  'Q1', 2024, FALSE),
(20240127, '2024-01-27', 'Saturday', 27, 1, 'January',  'Q1', 2024, TRUE),
(20240128, '2024-01-28', 'Sunday',   28, 1, 'January',  'Q1', 2024, TRUE),
(20240129, '2024-01-29', 'Monday',   29, 1, 'January',  'Q1', 2024, FALSE),
(20240130, '2024-01-30', 'Tuesday',  30, 1, 'January',  'Q1', 2024, FALSE),
(20240131, '2024-01-31', 'Wednesday',31, 1, 'January',  'Q1', 2024, FALSE),
(20240201, '2024-02-01', 'Thursday',  1, 2, 'February', 'Q1', 2024, FALSE),
(20240202, '2024-02-02', 'Friday',    2, 2, 'February', 'Q1', 2024, FALSE),
(20240203, '2024-02-03', 'Saturday',  3, 2, 'February', 'Q1', 2024, TRUE),
(20240204, '2024-02-04', 'Sunday',    4, 2, 'February', 'Q1', 2024, TRUE),
(20240205, '2024-02-05', 'Monday',    5, 2, 'February', 'Q1', 2024, FALSE),
(20240206, '2024-02-06', 'Tuesday',   6, 2, 'February', 'Q1', 2024, FALSE),
(20240207, '2024-02-07', 'Wednesday', 7, 2, 'February', 'Q1', 2024, FALSE),
(20240208, '2024-02-08', 'Thursday',  8, 2, 'February', 'Q1', 2024, FALSE),
(20240209, '2024-02-09', 'Friday',    9, 2, 'February', 'Q1', 2024, FALSE),
(20240210, '2024-02-10', 'Saturday', 10, 2, 'February', 'Q1', 2024, TRUE),
(20240211, '2024-02-11', 'Sunday',   11, 2, 'February', 'Q1', 2024, TRUE),
(20240212, '2024-02-12', 'Monday',   12, 2, 'February', 'Q1', 2024, FALSE),
(20240213, '2024-02-13', 'Tuesday',  13, 2, 'February', 'Q1', 2024, FALSE),
(20240214, '2024-02-14', 'Wednesday',14, 2, 'February', 'Q1', 2024, FALSE),
(20240215, '2024-02-15', 'Thursday', 15, 2, 'February', 'Q1', 2024, FALSE),
(20240216, '2024-02-16', 'Friday',   16, 2, 'February', 'Q1', 2024, FALSE),
(20240217, '2024-02-17', 'Saturday', 17, 2, 'February', 'Q1', 2024, TRUE),
(20240218, '2024-02-18', 'Sunday',   18, 2, 'February', 'Q1', 2024, TRUE);

-- ----------------------------
-- dim_product (15 products, 3 categories, varied prices 100–100000)
-- NOTE: product_key is identity; do not insert it.
-- ----------------------------
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('ELEC001', 'Laptop Pro 14',          'Electronics', 'Laptops',      85000.00),
('ELEC002', 'Smartphone X5',          'Electronics', 'Smartphones',  42000.00),
('ELEC003', 'NoiseCancel Headphones', 'Electronics', 'Audio',        18999.00),
('ELEC004', '4K Monitor 27',          'Electronics', 'Monitors',     32999.00),
('ELEC005', 'Smart TV 55 QLED',       'Electronics', 'Televisions',  64999.00),
('FASH001', 'Running Shoes',          'Fashion',     'Footwear',      4999.00),
('FASH002', 'Sneakers Classic',       'Fashion',     'Footwear',      7999.00),
('FASH003', 'Denim Jeans Slim Fit',   'Fashion',     'Clothing',      3499.00),
('FASH004', 'Formal Shirt Slim',      'Fashion',     'Clothing',      1999.00),
('FASH005', 'Trackpants Training',    'Fashion',     'Clothing',      2299.00),
('GROC001', 'Basmati Rice 5kg',       'Groceries',   'Staples',        650.00),
('GROC002', 'Organic Almonds 500g',   'Groceries',   'Dry Fruits',     899.00),
('GROC003', 'Organic Honey 500g',     'Groceries',   'Condiments',     450.00),
('GROC004', 'Masoor Dal 1kg',         'Groceries',   'Pulses',         120.00),
('GROC005', 'Olive Oil 1L',           'Groceries',   'Cooking',       1200.00);

-- ----------------------------
-- dim_customer (12 customers, 4 cities)
-- NOTE: customer_key is identity; do not insert it.
-- ----------------------------
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001', 'Rahul Sharma',     'Bangalore', 'Karnataka',   'Retail'),
('C002', 'Priya Patel',      'Mumbai',    'Maharashtra', 'Retail'),
('C003', 'Amit Kumar',       'Delhi',     'Delhi',       'Corporate'),
('C004', 'Sneha Reddy',      'Chennai',   'Tamil Nadu',  'Retail'),
('C005', 'Vikram Singh',     'Mumbai',    'Maharashtra', 'Premium'),
('C006', 'Anjali Mehta',     'Bangalore', 'Karnataka',   'Corporate'),
('C007', 'Ravi Verma',       'Delhi',     'Delhi',       'Retail'),
('C008', 'Pooja Iyer',       'Chennai',   'Tamil Nadu',  'Retail'),
('C009', 'Karthik Nair',     'Bangalore', 'Karnataka',   'Premium'),
('C010', 'Deepa Gupta',      'Delhi',     'Delhi',       'Retail'),
('C011', 'Arjun Rao',        'Chennai',   'Tamil Nadu',  'Corporate'),
('C012', 'Lakshmi Krishnan', 'Mumbai',    'Maharashtra', 'Premium');

-- ----------------------------
-- fact_sales (40 transactions)
-- ----------------------------
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES

(20240120, 2,  2, 1, 42000.00, 1000.00, 41000.00),
(20240120, 1,  5, 1, 85000.00, 5000.00, 80000.00),
(20240120, 6,  1, 2,  4999.00,  500.00,  9498.00),
(20240121, 4,  9, 1, 32999.00, 2000.00, 30999.00),
(20240121, 11, 12, 5,   650.00,    0.00,  3250.00),
(20240121, 3,  6, 1, 18999.00, 1000.00, 17999.00),
(20240122, 8,  2, 2,  3499.00,  200.00,  6798.00),
(20240123, 12, 5, 1,   899.00,    0.00,   899.00),
(20240124, 5,  3, 1, 64999.00, 3000.00, 61999.00),
(20240125, 14, 7, 8,   120.00,    0.00,   960.00),
(20240126, 9,  4, 3,  1999.00,  150.00,  5847.00),
(20240127, 1,  2, 1, 85000.00, 7000.00, 78000.00),
(20240127, 7,  9, 1,  7999.00,  500.00,  7499.00),
(20240128, 2,  5, 1, 42000.00, 2000.00, 40000.00),
(20240128, 15, 8, 2,  1200.00,   50.00,  2350.00),
(20240129, 10, 1, 2,  2299.00,  200.00,  4398.00),
(20240130, 13, 6, 3,   450.00,    0.00,  1350.00),
(20240131, 4,  3, 1, 32999.00, 1000.00, 31999.00),
(20240201, 5,  11,1, 64999.00, 2500.00, 62499.00),
(20240202, 3,  2, 1, 18999.00,  500.00, 18499.00),
(20240203, 2,  12,2, 42000.00, 3000.00, 81000.00),
(20240203, 6,  8, 3,  4999.00,  300.00, 14697.00),
(20240203, 11, 4, 10,  650.00,    0.00,  6500.00),
(20240204, 1,  5, 1, 85000.00, 5000.00, 80000.00),
(20240204, 9,  7, 2,  1999.00,  100.00,  3898.00),
(20240204, 12, 1, 1,   899.00,    0.00,   899.00),
(20240205, 8,  2, 1,  3499.00,  200.00,  3299.00),
(20240206, 4,  6, 1, 32999.00, 1500.00, 31499.00),
(20240207, 7,  9, 2,  7999.00,  500.00, 15498.00),
(20240208, 13, 10,4,   450.00,    0.00,  1800.00),
(20240209, 5,  3, 1, 64999.00, 2000.00, 62999.00),
(20240210, 2,  5, 1, 42000.00, 1500.00, 40500.00),
(20240210, 3,  12,1, 18999.00,  999.00, 18000.00),
(20240211, 1,  11,1, 85000.00, 6000.00, 79000.00),
(20240211, 14, 8, 12,  120.00,    0.00,  1440.00),
(20240212, 6,  2, 1,  4999.00,  200.00,  4799.00),
(20240213, 15, 4, 1,  1200.00,    0.00,  1200.00),
(20240214, 9,  7, 2,  1999.00,   99.00,  3899.00),
(20240215, 4,  6, 1, 32999.00,  999.00, 32000.00),
(20240216, 5,  5, 1, 64999.00, 5000.00, 59999.00),
(20240217, 2,  9, 1, 42000.00, 1000.00, 41000.00),
(20240217, 11, 12,6,   650.00,    0.00,  3900.00),
(20240218, 1,  3, 1, 85000.00, 8000.00, 77000.00),
(20240218, 3,  2, 1, 18999.00,  999.00, 18000.00);

COMMIT;
