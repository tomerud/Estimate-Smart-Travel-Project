import mysql.connector
from geopy.distance import geodesic
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Database connection configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# Establish the connection to the database
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_NAME
    )


# Function to create a dynamic table and insert distances
def calculate_distance_and_insert(city_name):
    # Connect to the database
    db = connect_db()
    cursor = db.cursor()

    # Normalize city name to create a valid table name (replace spaces with underscores)
    table_name = "distance_from_" + city_name.replace(" ", "_").lower()

    # Check if the table already exists, if so, drop it
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Creating table {table_name}...")

    # Create a new table for distances with dest_id as PRIMARY KEY and distance column
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            dest_id INT PRIMARY KEY,
            distance DECIMAL(10, 2)
        )
    """)

    # Fetch the latitude and longitude of the given city
    cursor.execute("""
        SELECT latitude, longitude 
        FROM top_touristic_cities 
        WHERE city = %s
    """, (city_name,))
    origin_data = cursor.fetchone()

    if not origin_data:
        print(f"City {city_name} not found in the database.")
        return

    origin_lat, origin_lon = origin_data

    # Fetch all other cities in the database
    cursor.execute("""
        SELECT city_id, latitude, longitude
        FROM top_touristic_cities
        WHERE city != %s
    """, (city_name,))

    cities = cursor.fetchall()

    # Iterate over all cities to calculate the distance
    for city_id, dest_lat, dest_lon in cities:
        # Calculate the distance using geopy's geodesic function
        distance = geodesic((origin_lat, origin_lon), (dest_lat, dest_lon)).kilometers

        # Insert the calculated distance into the new table
        cursor.execute(f"""
            INSERT INTO {table_name} (dest_id, distance)
            VALUES (%s, %s)
        """, (city_id, distance))

    # Commit the transaction
    db.commit()

    print(f"Distances for {city_name} to all other cities have been inserted into {table_name}.")

    # Close the connection
    cursor.close()
    db.close()


# Example Usage
# Calculate and insert the distance from 'Tel Aviv' into a dynamically created table
calculate_distance_and_insert('Las Vegas')
