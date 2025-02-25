import sqlite3
import os
from datetime import datetime

# Define database file path
DB_FILE = "mosquito_data.db"

# Ensure database directory exists
if not os.path.exists("database"):
    os.makedirs("database")

DB_PATH = os.path.join("database", DB_FILE)


# Function to initialize database
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            faa_count INTEGER NOT NULL,
            temperature_c REAL NOT NULL,
            raw_image_path TEXT NOT NULL,
            output_image_path TEXT NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()


# Function to insert a new detection record
def insert_detection(faa_count, temperature, raw_image_path, output_image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO detections (timestamp, faa_count, temperature_c, raw_image_path, output_image_path)
        VALUES (?, ?, ?, ?, ?)
    """,
        (timestamp, faa_count, temperature, raw_image_path, output_image_path),
    )

    conn.commit()
    conn.close()

    print(f"✅ Data saved to database: FAA={faa_count}, Temp={temperature}°C")


# Function to fetch all records from the database
def fetch_all_detections():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM detections ORDER BY timestamp DESC")
    records = cursor.fetchall()

    conn.close()
    return records


# Initialize database when script runs
initialize_database()
