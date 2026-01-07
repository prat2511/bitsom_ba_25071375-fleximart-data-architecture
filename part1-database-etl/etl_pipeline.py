import os
import re
import sys
import logging
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# ----------------------------
# PATHS
# ----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

DATA_DIR = os.path.join(BASE_DIR, "data")

CUSTOMERS_CSV = os.path.join(DATA_DIR, "customers_raw.csv")
PRODUCTS_CSV = os.path.join(DATA_DIR, "products_raw.csv")
SALES_CSV = os.path.join(DATA_DIR, "sales_raw.csv")

REPORT_FILE = os.path.join(SCRIPT_DIR, "data_quality_report.txt")
LOG_FILE = os.path.join(SCRIPT_DIR, "etl.log")


# ----------------------------
# LOGGING
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)


# ----------------------------
# DB CONFIG
# ----------------------------
PG_USER = "postgres"
PG_PASSWORD = "Welcome123"
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "fleximart"


def make_engine():
    url = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    return create_engine(url, future=True)


def ensure_files_exist():
    missing = []
    for p in [CUSTOMERS_CSV, PRODUCTS_CSV, SALES_CSV]:
        if not os.path.exists(p):
            missing.append(p)
    if missing:
        raise FileNotFoundError("Missing required CSV file(s):\n" + "\n".join(missing))


def safe_read_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception as e:
        logging.error(f"Failed to read CSV: {path}. Error: {e}")
        raise


def normalize_phone(phone):
    """Convert phone to +91-XXXXXXXXXX when possible."""
    if pd.isna(phone):
        return None

    digits = re.sub(r"\D", "", str(phone).strip())

    # remove leading country code 91 (keep last 10)
    if digits.startswith("91") and len(digits) > 10:
        digits = digits[-10:]

    # remove leading 0 if number is longer than 10 digits
    if digits.startswith("0") and len(digits) > 10:
        digits = digits[-10:]

    if len(digits) == 10:
        return f"+91-{digits}"
    return digits if digits else None


def standardize_category(x):
    if pd.isna(x):
        return "Unknown"
    v = str(x).strip().lower()
    mapping = {
        "electronics": "Electronics",
        "fashion": "Fashion",
        "groceries": "Groceries",
    }
    return mapping.get(v, str(x).strip().title())


def generate_email(first_name, last_name, raw_customer_code):
    fn = (str(first_name).strip().lower() or "customer")
    ln = (str(last_name).strip().lower() or "unknown")
    code = str(raw_customer_code).strip().lower()
    return f"{fn}.{ln}.{code}@unknown.email"

def parse_mixed_date(series: pd.Series) -> pd.Series:
    """
    Safely parse mixed date formats used in the assignment:
    - YYYY-MM-DD   (2024-01-15)
    - DD/MM/YYYY   (15/01/2024)
    - MM/DD/YYYY   (03/12/2024)
    - MM-DD-YYYY   (01-22-2024)
    """
    # Ensure string values and preserve original index
    s = series.astype(str).str.strip()
    s = s.copy()
    s.index = series.index

    # Output series with same index
    out = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")

    # YYYY-MM-DD
    m1 = s.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
    out.loc[m1] = pd.to_datetime(s.loc[m1], format="%Y-%m-%d", errors="coerce")

    # DD/MM/YYYY or MM/DD/YYYY
    m2 = s.str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)
    if m2.any():
        parts = s.loc[m2].str.split("/", expand=True)
        first = pd.to_numeric(parts[0], errors="coerce")

        # Day-first if first part > 12
        ddmm_mask = first > 12
        idx = s.loc[m2].index

        ddmm_idx = idx[ddmm_mask.values]
        mmdd_idx = idx[(~ddmm_mask).values]

        out.loc[ddmm_idx] = pd.to_datetime(s.loc[ddmm_idx], format="%d/%m/%Y", errors="coerce")
        out.loc[mmdd_idx] = pd.to_datetime(s.loc[mmdd_idx], format="%m/%d/%Y", errors="coerce")

    # MM-DD-YYYY
    m3 = s.str.match(r"^\d{2}-\d{2}-\d{4}$", na=False)
    out.loc[m3] = pd.to_datetime(s.loc[m3], format="%m-%d-%Y", errors="coerce")

    return out.dt.date

def write_report(lines):
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    logging.info("ETL started.")
    report = []

    try:
        # ----------------------------
        # PRECHECK
        # ----------------------------
        ensure_files_exist()
        logging.info("All input CSV files found.")

        # ----------------------------
        # EXTRACT
        # ----------------------------
        customers_raw = safe_read_csv(CUSTOMERS_CSV)
        products_raw = safe_read_csv(PRODUCTS_CSV)
        sales_raw = safe_read_csv(SALES_CSV)

        report.append("DATA QUALITY REPORT - FlexiMart ETL")
        report.append(f"Run timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("Records read:")
        report.append(f"  customers_raw.csv: {len(customers_raw)}")
        report.append(f"  products_raw.csv:  {len(products_raw)}")
        report.append(f"  sales_raw.csv:     {len(sales_raw)}")
        report.append("")

        logging.info(f"Read customers: {len(customers_raw)} rows")
        logging.info(f"Read products : {len(products_raw)} rows")
        logging.info(f"Read sales    : {len(sales_raw)} rows")

        # ----------------------------
        # TRANSFORM - CUSTOMERS
        # ----------------------------
        cust = customers_raw.copy()
        cust_dups = int(cust.duplicated().sum())
        cust = cust.drop_duplicates()

        cust["first_name"] = cust["first_name"].astype(str).str.strip()
        cust["last_name"] = cust["last_name"].astype(str).str.strip()
        cust["city"] = cust["city"].astype(str).str.strip().str.title()
        cust["phone"] = cust["phone"].apply(normalize_phone)
        cust["registration_date"] = parse_mixed_date(cust["registration_date"])

        cust["email"] = cust["email"].replace("", pd.NA)
        missing_email_before = int(cust["email"].isna().sum())

        cust["email"] = cust.apply(
            lambda r: generate_email(r["first_name"], r["last_name"], r["customer_id"])
            if pd.isna(r["email"]) else str(r["email"]).strip().lower(),
            axis=1,
        )

        # enforce uniqueness if any duplicates happen
        if cust["email"].duplicated().any():
            counts = {}
            fixed = []
            for e in cust["email"].tolist():
                if e not in counts:
                    counts[e] = 0
                    fixed.append(e)
                else:
                    counts[e] += 1
                    user, domain = e.split("@", 1)
                    fixed.append(f"{user}+{counts[e]}@{domain}")
            cust["email"] = fixed

        report.append("Customers cleaning:")
        report.append(f"  Duplicate rows removed: {cust_dups}")
        report.append(f"  Missing emails handled: {missing_email_before} -> filled with placeholders (@unknown.email)")
        report.append("")

        logging.info(f"Customers duplicates removed: {cust_dups}")
        logging.info(f"Customers missing emails filled: {missing_email_before}")
        logging.info(f"Customers rows after cleaning: {len(cust)}")

        # ----------------------------
        # TRANSFORM - PRODUCTS
        # ----------------------------
        prod = products_raw.copy()
        prod_dups = int(prod.duplicated().sum())
        prod = prod.drop_duplicates()

        prod["product_name"] = prod["product_name"].astype(str).str.strip()
        prod["category"] = prod["category"].apply(standardize_category)

        prod["price"] = pd.to_numeric(prod["price"], errors="coerce")
        missing_price_before = int(prod["price"].isna().sum())

        # fill missing price with category median, fallback overall median
        overall_median = prod["price"].median(skipna=True)
        med_by_cat = prod.groupby("category")["price"].median()

        def fill_price(row):
            if pd.isna(row["price"]):
                cm = med_by_cat.get(row["category"], pd.NA)
                if pd.notna(cm):
                    return float(cm)
                if pd.notna(overall_median):
                    return float(overall_median)
                return 0.0
            return float(row["price"])

        prod["price"] = prod.apply(fill_price, axis=1)

        prod["stock_quantity"] = pd.to_numeric(prod["stock_quantity"], errors="coerce")
        missing_stock_before = int(prod["stock_quantity"].isna().sum())
        prod["stock_quantity"] = prod["stock_quantity"].fillna(0).astype(int)

        report.append("Products cleaning:")
        report.append(f"  Duplicate rows removed: {prod_dups}")
        report.append(f"  Missing prices handled: {missing_price_before} -> filled using category median (fallback overall median)")
        report.append(f"  Missing stock handled:  {missing_stock_before} -> filled with 0")
        report.append("")

        logging.info(f"Products duplicates removed: {prod_dups}")
        logging.info(f"Products missing prices filled: {missing_price_before}")
        logging.info(f"Products missing stock filled: {missing_stock_before}")
        logging.info(f"Products rows after cleaning: {len(prod)}")

        # ----------------------------
        # TRANSFORM - SALES
        # ----------------------------
        sales = sales_raw.copy()
        sales_dups = int(sales.duplicated().sum())
        sales = sales.drop_duplicates()

        sales["transaction_date"] = parse_mixed_date(sales["transaction_date"])

        # Drop rows missing customer_id/product_id (FK cannot be satisfied)
        missing_cust = sales["customer_id"].isna() | (sales["customer_id"].astype(str).str.strip() == "")
        missing_prod = sales["product_id"].isna() | (sales["product_id"].astype(str).str.strip() == "")
        dropped_missing_ids = int((missing_cust | missing_prod).sum())
        sales = sales[~(missing_cust | missing_prod)].copy()

        # Drop rows where date couldn't be parsed (orders.order_date is NOT NULL)
        before_date_drop = len(sales)
        sales = sales.dropna(subset=["transaction_date"])
        dropped_bad_dates = before_date_drop - len(sales)

        sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce").fillna(0).astype(int)
        sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce").fillna(0.0).astype(float)
        sales["subtotal"] = sales["quantity"] * sales["unit_price"]

        report.append("Sales cleaning:")
        report.append(f"  Duplicate rows removed: {sales_dups}")
        report.append(f"  Rows dropped (missing customer_id/product_id): {dropped_missing_ids}")
        report.append(f"  Rows dropped (unparsed dates): {dropped_bad_dates}")
        report.append("")

        logging.info(f"Sales duplicates removed: {sales_dups}")
        logging.info(f"Sales rows dropped (missing IDs): {dropped_missing_ids}")
        logging.info(f"Sales rows dropped (bad dates): {dropped_bad_dates}")
        logging.info(f"Sales rows after cleaning: {len(sales)}")

        # ----------------------------
        # LOAD
        # ----------------------------
        engine = make_engine()

        # Test DB connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        logging.info("Database connection successful.")

        with engine.begin() as conn:
            logging.info("Starting database load transaction...")

            conn.execute(text("TRUNCATE TABLE order_items RESTART IDENTITY CASCADE;"))
            conn.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE;"))
            conn.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))
            conn.execute(text("TRUNCATE TABLE customers RESTART IDENTITY CASCADE;"))

            # Insert customers
            cust_insert = cust[["first_name", "last_name", "email", "phone", "city", "registration_date"]].copy()
            cust_insert.to_sql("customers", conn, if_exists="append", index=False)

            # Map raw customer code -> surrogate customer_id using email
            db_customers = pd.read_sql("SELECT customer_id, email FROM customers", conn)
            temp_cust = cust[["customer_id", "email"]].copy()
            temp_cust = temp_cust.rename(columns={"customer_id": "raw_customer_code"})
            temp_cust["email"] = temp_cust["email"].astype(str).str.lower().str.strip()

            db_customers["email"] = db_customers["email"].astype(str).str.lower().str.strip()
            db_customers = db_customers.rename(columns={"customer_id": "surrogate_customer_id"})

            temp_cust = temp_cust.merge(db_customers, on="email", how="left")
            raw_customer_to_surrogate = dict(zip(temp_cust["raw_customer_code"], temp_cust["surrogate_customer_id"]))

            # Insert products
            prod_insert = prod[["product_name", "category", "price", "stock_quantity"]].copy()
            prod_insert.to_sql("products", conn, if_exists="append", index=False)

            # Map raw product code -> surrogate product_id using product_name+category+price
            db_products = pd.read_sql("SELECT product_id, product_name, category, price FROM products", conn)
            key = prod[["product_id", "product_name", "category", "price"]].copy()
            key = key.rename(columns={"product_id": "raw_product_code"})
            db_products = db_products.rename(columns={"product_id": "surrogate_product_id"})

            key = key.merge(db_products, on=["product_name", "category", "price"], how="left")
            raw_product_to_surrogate = dict(zip(key["raw_product_code"], key["surrogate_product_id"]))

            # Build orders (one per transaction_id)
            orders_df = sales[["transaction_id", "customer_id", "transaction_date", "status"]].copy()
            orders_df["customer_id"] = orders_df["customer_id"].map(raw_customer_to_surrogate)

            # Safety: drop any unmapped customers (should be 0)
            before_orders = len(orders_df)
            orders_df = orders_df[orders_df["customer_id"].notna()].copy()
            dropped_unmapped_customers = before_orders - len(orders_df)

            totals = sales.groupby("transaction_id")["subtotal"].sum().reset_index()
            orders_df = orders_df.merge(totals, on="transaction_id", how="left")

            orders_df = orders_df.rename(columns={"transaction_date": "order_date", "subtotal": "total_amount"})
            orders_insert = orders_df[["customer_id", "order_date", "total_amount", "status"]].copy()
            orders_insert.to_sql("orders", conn, if_exists="append", index=False)

            # Fetch order_id back (match on all fields)
            db_orders = pd.read_sql("SELECT order_id, customer_id, order_date, total_amount, status FROM orders", conn)
            orders_df = orders_df.merge(db_orders, on=["customer_id", "order_date", "total_amount", "status"], how="left")
            tx_to_order_id = dict(zip(orders_df["transaction_id"], orders_df["order_id"]))

            # Build order_items (one row per sales record)
            items = sales[["transaction_id", "product_id", "quantity", "unit_price", "subtotal"]].copy()
            items["order_id"] = items["transaction_id"].map(tx_to_order_id)
            items["product_id"] = items["product_id"].map(raw_product_to_surrogate)

            before_items = len(items)
            items = items[items["order_id"].notna() & items["product_id"].notna()].copy()
            dropped_unmapped_products = before_items - len(items)

            items_insert = items[["order_id", "product_id", "quantity", "unit_price", "subtotal"]].copy()
            items_insert.to_sql("order_items", conn, if_exists="append", index=False)

            logging.info("Database load committed successfully.")

        # ----------------------------
        # FINAL COUNTS + REPORT
        # ----------------------------
        with engine.connect() as conn:
            c_cnt = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar_one()
            p_cnt = conn.execute(text("SELECT COUNT(*) FROM products")).scalar_one()
            o_cnt = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar_one()
            oi_cnt = conn.execute(text("SELECT COUNT(*) FROM order_items")).scalar_one()

        report.append("Load results:")
        report.append(f"  customers loaded:   {c_cnt}")
        report.append(f"  products loaded:    {p_cnt}")
        report.append(f"  orders loaded:      {o_cnt}")
        report.append(f"  order_items loaded: {oi_cnt}")
        report.append("")
        report.append("Notes:")
        report.append("  - Sales rows with missing customer_id/product_id were dropped to satisfy FK constraints.")
        report.append("  - Sales rows with unparseable dates were dropped because orders.order_date is NOT NULL.")
        report.append("  - Missing customer emails were generated as placeholders to satisfy NOT NULL + UNIQUE constraint.")
        report.append("  - Missing prices filled using category median (fallback overall median).")
        report.append(f"  - Unmapped customers dropped during order load (safety): {dropped_unmapped_customers}")
        report.append(f"  - Unmapped products dropped during item load (safety): {dropped_unmapped_products}")

        write_report(report)

        logging.info("ETL complete.")
        logging.info(f"Report written to: {REPORT_FILE}")
        logging.info(f"Log written to: {LOG_FILE}")

    except FileNotFoundError as e:
        logging.error(f"INPUT FILE ERROR: {e}")
        raise
    except SQLAlchemyError as e:
        logging.error(f"DATABASE ERROR: {e}")
        raise
    except Exception as e:
        logging.error(f"UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
