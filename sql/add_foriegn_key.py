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

# Define SQL queries to add foreign keys with ON DELETE CASCADE
add_foreign_key_weather = """
ALTER TABLE weather
ADD CONSTRAINT fk_weather_city
FOREIGN KEY (city) REFERENCES top_touristic_cities(city)
ON DELETE CASCADE;
"""

add_foreign_key_beach_cities = """
ALTER TABLE beach_cities
ADD CONSTRAINT fk_beach_city
FOREIGN KEY (city_name) REFERENCES top_touristic_cities(city)
ON DELETE CASCADE;
"""

# Execute the queries to add the foreign keys
try:
    cursor.execute(add_foreign_key_weather)
    print("Foreign key added to 'weather' table.")
except mysql.connector.Error as err:
    print(f"Error adding foreign key to 'weather': {err}")

try:
    cursor.execute(add_foreign_key_beach_cities)
    print("Foreign key added to 'beach_cities' table.")
except mysql.connector.Error as err:
    print(f"Error adding foreign key to 'beach_cities': {err}")

# Commit changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
