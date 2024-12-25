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

# List of cities with amazing or crazy nightlife scene
party_cities_list = [
     "Belgrade", # Added Belgrade
    "Havana"   
]

# SQL query to insert a city into the 'party_cities' table
insert_query = """
INSERT INTO party_cities (city) 
VALUES (%s);
"""

# Insert each city into the table
for city in party_cities_list:
    cursor.execute(insert_query, (city,))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print(f"Cities with amazing nightlife added to 'party_cities' table successfully.")
