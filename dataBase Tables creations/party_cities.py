from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables from .env file
load_dotenv()

# Connect to MySQL using environment variables
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", 3306)),  # Default to 3306 if not set
    database=os.getenv("DB_NAME")
)

# Create a cursor
cursor = conn.cursor()

# SQL query to create the 'party_cities' table with a foreign key
create_table_query = """
CREATE TABLE IF NOT EXISTS party_cities (
    city VARCHAR(100),
    PRIMARY KEY (city),
    FOREIGN KEY (city) REFERENCES top_touristic_cities(city)
);
"""

# Execute the query to create the table
cursor.execute(create_table_query)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Table 'party_cities' created successfully.")
