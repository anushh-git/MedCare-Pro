import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS MedicineInventory (
    Medicine TEXT,
    Category TEXT,
    Supplier TEXT,
    Quantity INTEGER,
    Min_Stock INTEGER,
    Unit_Price REAL,
    Total_Value REAL,
    Expiry_Date TEXT,
    Manufacturing_Date TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")