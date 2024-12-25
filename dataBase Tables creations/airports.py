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

# SQL query to create the airports table with airport_name
create_airports_table_query = """
CREATE TABLE IF NOT EXISTS airports (
    iata_code VARCHAR(10) PRIMARY KEY,
    airport_name VARCHAR(150),
    municipality VARCHAR(100),
    longitude DECIMAL(9, 6),
    latitude DECIMAL(9, 6),
    FOREIGN KEY (municipality) REFERENCES top_touristic_cities(city) ON DELETE CASCADE
);
"""

# Execute the query to create the table
cursor.execute(create_airports_table_query)
conn.commit()

print("Table 'airports' created successfully.")

# Close the cursor and connection
cursor.close()
conn.close()
