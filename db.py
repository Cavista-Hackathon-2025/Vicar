import sqlite3
from datetime import datetime
import os
from typing import List, Tuple, Optional

# Database configuration
DB_PATH = os.getenv("DB_PATH", "pharmacy.db")
API_BASE_URL = os.getenv("NGROK_URL", f"http://127.0.0.1:{os.getenv('PORT', 5000)}")

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

def init_db() -> None:
    """Initialize the database with required tables."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                drug TEXT PRIMARY KEY,
                units_left INTEGER,
                restock_at INTEGER,
                last_updated TEXT,
                initial_units INTEGER,
                batch_number TEXT,
                api_endpoint TEXT
            )''')
            conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to initialize database: {e}")

def update_stock(drug: str, units_left: int, restock_at: int, batch_number: str) -> Tuple[Optional[str], int]:
    """Update or insert stock information."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT last_updated, initial_units FROM inventory WHERE drug =?", (drug,))
            row = c.fetchone()
            last_updated = row[0] if row else None
            initial_units = row[1] if row else units_left

            now = datetime.now().isoformat()
            # Store the API endpoint for this record
            api_url = f"{API_BASE_URL}/api/update"
            
            c.execute("""
                INSERT OR REPLACE INTO inventory 
                (drug, units_left, restock_at, last_updated, initial_units, batch_number, api_endpoint)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (drug, units_left, restock_at, now, 
                  initial_units if not last_updated else initial_units, 
                  batch_number, api_url))
            conn.commit()
            return last_updated, initial_units
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to update stock: {e}")

def get_stock() -> List[Tuple]:
    """Retrieve all stock information."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT drug, units_left, restock_at, last_updated, 
                       initial_units, batch_number, api_endpoint 
                FROM inventory
            """)
            return c.fetchall()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to retrieve stock: {e}")

# function to get the current API base URL
def get_api_base_url() -> str:
    """Get the current API base URL (ngrok or localhost)"""
    return API_BASE_URL

if __name__ == "__main__":
    init_db()
    
    # Testing  multiple inserts
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
        print(f"API endpoint: {item[6]}")
        print("-" * 30)