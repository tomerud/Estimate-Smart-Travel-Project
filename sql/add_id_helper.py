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

# Step 1: Drop the existing primary key on `city`
cursor.execute("""
    ALTER TABLE top_touristic_cities DROP PRIMARY KEY;
""")
conn.commit()

# Step 2: Add `city_id` column and set it as the primary key
cursor.execute("""
    ALTER TABLE top_touristic_cities
    ADD COLUMN city_id INT AUTO_INCREMENT PRIMARY KEY FIRST;
""")
conn.commit()

# Commit changes and close the cursor and connection
cursor.close()
conn.close()
