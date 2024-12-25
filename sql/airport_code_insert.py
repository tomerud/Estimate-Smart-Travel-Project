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

# Step 1: Select all cities and their airport codes from the airports table
select_airports_query = "SELECT municipality, iata_code FROM airports"
cursor.execute(select_airports_query)
airport_data = cursor.fetchall()

# Step 2: Update tel_aviv_flights with the airport_code for each city
update_flight_query = "UPDATE tel_aviv_flights SET airport_code = %s WHERE destination = %s"
for municipality, iata_code in airport_data:
    cursor.execute(update_flight_query, (iata_code, municipality))
    print(f"Updated {municipality} in tel_aviv_flights with airport code: {iata_code}")

# Commit the changes
conn.commit()

print("Updated 'tel_aviv_flights' with airport codes from 'airports' table.")

# Close the cursor and connection
cursor.close()
conn.close()
