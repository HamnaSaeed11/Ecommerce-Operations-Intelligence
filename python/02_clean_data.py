
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Create processed folder if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load all datasets
files = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

data = {}

for file in files:
    data[file] = pd.read_csv(RAW_DIR / file)
    print(f"Loaded {file}: {len(data[file])} rows")


# 1. Remove exact duplicate geolocation records
geo_file = "olist_geolocation_dataset.csv"

before = len(data[geo_file])

data[geo_file] = data[geo_file].drop_duplicates()

after = len(data[geo_file])

print("\nGeolocation duplicate records removed:", before - after)


# 2. Convert order timestamps into datetime
orders_file = "olist_orders_dataset.csv"

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    data[orders_file][column] = pd.to_datetime(
        data[orders_file][column],
        errors="coerce"
    )


# 3. Convert shipping and review dates
items_file = "olist_order_items_dataset.csv"

data[items_file]["shipping_limit_date"] = pd.to_datetime(
    data[items_file]["shipping_limit_date"],
    errors="coerce"
)

reviews_file = "olist_order_reviews_dataset.csv"

review_date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in review_date_columns:
    data[reviews_file][column] = pd.to_datetime(
        data[reviews_file][column],
        errors="coerce"
    )


# 4. Fill missing product categories
products_file = "olist_products_dataset.csv"

data[products_file]["product_category_name"] = (
    data[products_file]["product_category_name"].fillna("Unknown")
)


# 5. Convert numerical columns
numeric_columns = {
    items_file: ["order_item_id", "price", "freight_value"],
    "olist_order_payments_dataset.csv": [
        "payment_sequential",
        "payment_installments",
        "payment_value"
    ],
    products_file: [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ],
    reviews_file: ["review_score"]
}

for file, columns in numeric_columns.items():
    for column in columns:
        data[file][column] = pd.to_numeric(
            data[file][column],
            errors="coerce"
        )


# 6. Check duplicate review IDs without deleting records
duplicate_review_ids = data[reviews_file][
    "review_id"
].duplicated().sum()

print("\nRepeated review IDs:", duplicate_review_ids)


# 7. Export cleaned datasets
for file, df in data.items():
    output_path = PROCESSED_DIR / file
    df.to_csv(output_path, index=False)

    print(f"Saved: {file} | Rows: {len(df)}")


print("\nData cleaning completed successfully!")

# 8. Validate cleaned datasets

print("\n========== CLEANING VALIDATION ==========")

# Check remaining exact duplicates in geolocation
print(
    "Remaining geolocation duplicates:",
    data[geo_file].duplicated().sum()
)

# Check missing product categories
print(
    "Missing product categories:",
    data[products_file]["product_category_name"].isna().sum()
)

# Check product categories marked as Unknown
print(
    "Unknown product categories:",
    (data[products_file]["product_category_name"] == "Unknown").sum()
)

# Check missing delivery dates
print(
    "Missing customer delivery dates:",
    data[orders_file]["order_delivered_customer_date"].isna().sum()
)

# Check date column data type
print(
    "Purchase timestamp data type:",
    data[orders_file]["order_purchase_timestamp"].dtype
)

print("\nValidation completed!")

