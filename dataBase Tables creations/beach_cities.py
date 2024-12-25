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

# Define the SQL query to create the beach_cities table with an empty structure
create_table_query = """
CREATE TABLE IF NOT EXISTS beach_cities (
    city_name VARCHAR(100) PRIMARY KEY
);
"""

# Execute the query to create the table
cursor.execute(create_table_query)
conn.commit()

print("Empty 'beach_cities' table created with a 'city_name' column.")

# Close the cursor and connection
cursor.close()
conn.close()
