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

# Step 1: Select all cities from top_touristic_cities
select_cities_query = "SELECT city FROM top_touristic_cities"
cursor.execute(select_cities_query)
cities = cursor.fetchall()

# Step 2: Insert each city into tel_aviv_flights with other columns as NULL
insert_flight_query = "INSERT INTO tel_aviv_flights (destination) VALUES (%s)"
for city in cities:
    cursor.execute(insert_flight_query, (city[0],))  # city[0] extracts the city name from the tuple
    print(f"Inserted city: {city[0]} into tel_aviv_flights")

# Commit the changes
conn.commit()

print("All cities from 'top_touristic_cities' added to 'tel_aviv_flights' with other columns as NULL.")

# Close the cursor and connection
cursor.close()
conn.close()
