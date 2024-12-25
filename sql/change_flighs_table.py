import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to the MySQL database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Step 1: Drop the current 'airport' column
alter_table_drop_column_query = "ALTER TABLE tel_aviv_flights DROP COLUMN airport;"
cursor.execute(alter_table_drop_column_query)

# Step 2: Add the new 'airport_code' column
alter_table_add_column_query = """
ALTER TABLE tel_aviv_flights
ADD COLUMN airport_code VARCHAR(10),
ADD CONSTRAINT fk_airport_code
FOREIGN KEY (airport_code) REFERENCES airports(iata_code)
ON DELETE SET NULL;
"""
cursor.execute(alter_table_add_column_query)

# Commit the changes
conn.commit()

print("Table 'tel_aviv_flights' modified successfully: 'airport_code' column added as a foreign key.")

# Close the cursor and connection
cursor.close()
conn.close()
