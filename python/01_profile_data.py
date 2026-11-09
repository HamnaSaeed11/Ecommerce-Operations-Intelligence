
import pandas as pd
from pathlib import Path
import gc

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Find all CSV files
csv_files = list(RAW_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files found in {RAW_DIR}. Check your folder."
    )

profile_results = []
missing_results = []

print(f"Found {len(csv_files)} CSV files\n")

for file in csv_files:

    print(f"Inspecting: {file.name}")

    df = pd.read_csv(file, low_memory=False)

    # General information
    profile_results.append({
        "file_name": file.name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicate_rows": df.duplicated().sum(),
        "total_missing_values": df.isna().sum().sum()
    })

    # Missing values for each column
    missing = df.isna().sum()

    for column, count in missing.items():
        missing_results.append({
            "file_name": file.name,
            "column_name": column,
            "missing_values": count,
            "missing_percentage": round(
                (count / len(df)) * 100, 2
            )
        })

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Duplicate rows:", df.duplicated().sum())
    print("Missing values:", df.isna().sum().sum())
    print("-" * 40)

    del df
    gc.collect()

# Save reports
profile_df = pd.DataFrame(profile_results)
missing_df = pd.DataFrame(missing_results)

profile_df.to_csv(
    REPORT_DIR / "dataset_profile.csv",
    index=False
)

missing_df.to_csv(
    REPORT_DIR / "missing_values_report.csv",
    index=False
)

print("\nData profiling completed!")
print("Reports saved inside the reports folder.")