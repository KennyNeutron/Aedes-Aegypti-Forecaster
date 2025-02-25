import sqlite3

# Define the path to your database
database_path = 'FAA_DB.db'

# Connect to SQLite Database
conn = sqlite3.connect(database_path)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# SQL command to create a table
sql_command = '''
CREATE TABLE IF NOT EXISTS MosquitoData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    faa_count INTEGER,
    temperature REAL
);
'''

# Execute the SQL command to create the table
cursor.execute(sql_command)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

# Print a success message
print("Database and table created successfully")
