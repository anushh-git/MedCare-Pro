import pandas as pd
import sqlite3

# Path to your Excel file
EXCEL_FILE = r"inventory.xlsx"

# Load Excel
df = pd.read_excel(EXCEL_FILE, engine="openpyxl")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# Connect to SQLite database
conn = sqlite3.connect("inventory.db")

# Push into database
df.to_sql(
    "MedicineInventory",
    conn,
    if_exists="replace",   # overwrites old empty table
    index=False
)

conn.close()

print("Excel data successfully loaded into database")
