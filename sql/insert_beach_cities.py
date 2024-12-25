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

# Define the beach cities (only city names)
beach_cities = [
    "Barcelona", "Cape Town", "Cartagena", "Dubai", "Eilat", "Fortaleza",
    "Havana", "Malaga", "Manila", "Miami", "Montevideo", "Muscat", "Nice",
    "Pattaya", "Phuket", "Recife", "Rio de Janeiro", "Salvador", "Singapore",
    "Sydney", "Tel Aviv", "Zanzibar City"
]

# Insert each city into the beach_cities table
insert_query = "INSERT IGNORE INTO beach_cities (city_name) VALUES (%s)"
for city in beach_cities:
    cursor.execute(insert_query, (city,))

conn.commit()

print("Beach cities have been added to the 'beach_cities' table.")

# Close the cursor and connection
cursor.close()
conn.close()
