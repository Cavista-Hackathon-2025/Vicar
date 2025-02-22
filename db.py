import sqlite3
from datetime import datetime

DB_PATH = "pharmacy.db"  # os.getenv('DB_PATH', '/home/user/pharmacy.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS inventory (
            drug TEXT PRIMARY KEY,
            units_left INTEGER,
            restock_at INTEGER,
            last_updated TEXT,
            initial_units INTEGER,
            batch_number TEXT
        )''')
        conn.commit()

def update_stock(drug, units_left, restock_at, batch_number):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT last_updated, initial_units FROM inventory WHERE drug =?", (drug,))
        row = c.fetchone()
        last_updated = row[0] if row else None
        initial_units = row[1] if row else units_left

        now = datetime.now().isoformat()
        c.execute("""
            INSERT OR REPLACE INTO inventory (drug, units_left, restock_at, last_updated, initial_units, batch_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (drug, units_left, restock_at, now, initial_units if not last_updated else initial_units, batch_number))
        conn.commit()
    return last_updated, initial_units

def get_stock():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT drug, units_left, restock_at, last_updated, initial_units, batch_number FROM inventory")
        rows = c.fetchall()
    return rows

if __name__ == "__main__":
    init_db()
    
    # Test multiple inserts
    test_drugs = [
        ("Paracetamol", 100, 20, "BATCH001"),
        ("Amoxicillin", 50, 10, "BATCH002"),
        ("Ibuprofen", 75, 15, "BATCH003")
    ]
    
    for drug, units, restock, batch in test_drugs:
        update_stock(drug, units, restock, batch)
    
    # Query and display results
    stock = get_stock()
    for item in stock:
        print(f"Drug: {item[0]}")
        print(f"Units left: {item[1]}")
        print(f"Restock at: {item[2]}")
        print(f"Last updated: {item[3]}")
        print(f"Initial units: {item[4]}")
        print(f"Batch number: {item[5]}")
        print("-" * 30)