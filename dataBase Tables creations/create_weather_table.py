import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

# Create a cursor object
cursor = conn.cursor()

# SQL query to create the `weather` table
create_weather_table_query = """
CREATE TABLE IF NOT EXISTS weather (
    city VARCHAR(100) PRIMARY KEY,
    january_avg_temp FLOAT,
    february_avg_temp FLOAT,
    march_avg_temp FLOAT,
    april_avg_temp FLOAT,
    may_avg_temp FLOAT,
    june_avg_temp FLOAT,
    july_avg_temp FLOAT,
    august_avg_temp FLOAT,
    september_avg_temp FLOAT,
    october_avg_temp FLOAT,
    november_avg_temp FLOAT,
    december_avg_temp FLOAT
);
"""

# Execute the query to create the table
cursor.execute(create_weather_table_query)

# Commit changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Table 'weather' created successfully.")
