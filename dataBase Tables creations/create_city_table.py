import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from ..env file
load_dotenv()

# Connect to MySQL database using environment variables
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

# Create a cursor object
cursor = conn.cursor()

# SQL query to create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS top_touristic_cities (
    city VARCHAR(100) PRIMARY KEY,
    country VARCHAR(100),
    continent VARCHAR(100),
    language VARCHAR(100),
    religion VARCHAR(100),
    human_development_index FLOAT,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6)
);
"""

# Execute the query to create the table
cursor.execute(create_table_query)

# Commit changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Table 'top_touristic_cities' created successfully.")
