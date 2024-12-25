import mysql.connector
from dotenv import load_dotenv
import os
import math

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


# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


# Step 1: Get all destinations with NULL airport_code from tel_aviv_flights
null_airports_query = """
SELECT destination, latitude, longitude
FROM top_touristic_cities
JOIN tel_aviv_flights ON top_touristic_cities.city = tel_aviv_flights.destination
WHERE tel_aviv_flights.airport_code IS NULL
"""
cursor.execute(null_airports_query)
null_airports = cursor.fetchall()

# Step 2: Get all airport data from the airports table
select_all_airports_query = "SELECT airport_name, iata_code, latitude, longitude FROM airports"
cursor.execute(select_all_airports_query)
all_airports = cursor.fetchall()

# Step 3: Find the closest airport for each destination with NULL airport_code
closest_airports = []  # List to store closest airport data for each destination

for destination, dest_lat, dest_lon in null_airports:
    closest_airport = None
    min_distance = float('inf')

    for airport_name, iata_code, airport_lat, airport_lon in all_airports:
        # Calculate distance between destination and airport
        distance = haversine(dest_lat, dest_lon, airport_lat, airport_lon)

        if distance < min_distance:
            min_distance = distance
            closest_airport = (destination, airport_name, iata_code, distance)

    # Append the closest airport data to the list
    if closest_airport:
        closest_airports.append(closest_airport)

# Step 4: Sort the list by distance
closest_airports.sort(key=lambda x: x[3])  # Sort by the distance (fourth element in the tuple)

# Step 5: Print the sorted closest airports
for destination, airport_name, iata_code, distance in closest_airports:
    print(f"Closest airport to {destination} is {airport_name} ({iata_code}) with distance {distance:.2f} km")

# Close the cursor and connection
cursor.close()
conn.close()
