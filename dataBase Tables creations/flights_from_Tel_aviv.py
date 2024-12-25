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

# Step 1: Drop the existing 'tel_aviv_flights' table if it exists
drop_table_query = "DROP TABLE IF EXISTS tel_aviv_flights;"
cursor.execute(drop_table_query)

# Step 2: Create the new 'tel_aviv_flights' table with 'destination' and 'airport_code' as foreign keys
create_table_query = """
CREATE TABLE tel_aviv_flights (
    destination VARCHAR(100),
    airport_code VARCHAR(10),
    january_avg_price DECIMAL(10,2),
    february_avg_price DECIMAL(10,2),
    march_avg_price DECIMAL(10,2),
    april_avg_price DECIMAL(10,2),
    may_avg_price DECIMAL(10,2),
    june_avg_price DECIMAL(10,2),
    july_avg_price DECIMAL(10,2),
    august_avg_price DECIMAL(10,2),
    september_avg_price DECIMAL(10,2),
    october_avg_price DECIMAL(10,2),
    november_avg_price DECIMAL(10,2),
    december_avg_price DECIMAL(10,2),
    PRIMARY KEY (destination),
    FOREIGN KEY (destination) REFERENCES top_touristic_cities(city) ON DELETE CASCADE,
    FOREIGN KEY (airport_code) REFERENCES airports(iata_code) ON DELETE SET NULL
);
"""
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

print("Table 'tel_aviv_flights' created successfully with 'destination' as a foreign key to 'top_touristic_cities' and 'airport_code' as a foreign key to 'airports'.")

# Close the cursor and connection
cursor.close()
conn.close()
