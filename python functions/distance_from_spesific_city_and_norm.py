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

# Function to create a dynamic table, calculate distances and insert into the table with normalization
def calculate_distance_and_insert(city_name):
    # Connect to the database
    db = connect_db()
    cursor = db.cursor()

    # Normalize city name to create a valid table name (replace spaces with underscores)
    table_name = "distance_from_" + city_name.replace(" ", "_").lower()

    # Drop the old table if it exists and create a new one
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Creating table {table_name}...")

    # Create a new table for distances with dest_id as PRIMARY KEY, distance, and norm_dist columns
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            dest_id INT PRIMARY KEY,
            distance DECIMAL(10, 2),
            norm_dist DECIMAL(10, 2)
        )
    """)

    # Fetch the latitude and longitude of the given city
    cursor.execute("""
        SELECT city_id, latitude, longitude 
        FROM top_touristic_cities 
        WHERE city = %s
    """, (city_name,))
    origin_data = cursor.fetchone()

    if not origin_data:
        print(f"City {city_name} not found in the database.")
        return

    origin_id, origin_lat, origin_lon = origin_data

    # Fetch all cities in the database, including the given city itself
    cursor.execute("""
        SELECT city_id, latitude, longitude
        FROM top_touristic_cities
    """)
    cities = cursor.fetchall()

    # List to hold distances for later normalization
    distances = []

    # Iterate over all cities to calculate the distance
    for city_id, dest_lat, dest_lon in cities:
        # Calculate the distance using geopy's geodesic function
        if city_id == origin_id:
            distance = 0  # Distance to itself is 0
        else:
            distance = geodesic((origin_lat, origin_lon), (dest_lat, dest_lon)).kilometers
        distances.append(distance)

        # Insert the calculated distance into the new table (without normalization yet)
        cursor.execute(f"""
            INSERT INTO {table_name} (dest_id, distance)
            VALUES (%s, %s)
        """, (city_id, distance))

    # Normalize the distances between 0 and 1
    if distances:
        min_distance = min(distances)
        max_distance = max(distances)

        # Update the norm_dist column for all rows
        for idx, city_id in enumerate([city[0] for city in cities]):
            normalized_distance = (distances[idx] - min_distance) / (max_distance - min_distance) if max_distance > min_distance else 0
            cursor.execute(f"""
                UPDATE {table_name} 
                SET norm_dist = %s 
                WHERE dest_id = %s
            """, (normalized_distance, city_id))

    # Commit the transaction
    db.commit()

    print(f"Distances for {city_name} to all cities (including itself) have been inserted into {table_name} with normalization.")

    # Close the connection
    cursor.close()
    db.close()



# Example Usage
# Calculate and insert the distance from 'Tel Aviv' into a dynamically created table with normalized distances


# List of cities to process
cities_to_process = [
    'Abu Dhabi', 'Accra', 'Almaty', 'Amman', 'Amsterdam', 'Antofagasta', 'Antwerp', 'Arequipa', 'Asunción',
    'Athens', 'Auckland', 'Bangalore', 'Bangkok', 'Barcelona', 'Basel', 'Beijing', 'Beirut', 'Belgrade', 'Bergen',
    'Berlin', 'Bogotá', 'Bologna', 'Brasilia', 'Bratislava', 'Brussels', 'Budapest', 'Buenos Aires', 'Cairo',
    'Cape Town', 'Cartagena', 'Casablanca', 'Chengdu', 'Chennai', 'Chiang Mai', 'Chicago', 'Córdoba', 'Cusco',
    'Dakar', 'Delhi', 'Doha', 'Dubai', 'Dublin', 'Edinburgh', 'Eilat', 'Fes', 'Florence', 'Fortaleza', 'Geneva',
    'Ghent', 'Guangzhou', 'Guayaquil', 'Hamburg', 'Hanoi', 'Havana', 'Helsinki', 'Hiroshima', 'Ho Chi Minh City',
    'Hobart', 'Hong Kong', 'Innsbruck', 'Istanbul', 'Jaipur', 'Jakarta', 'Jerusalem', 'Johannesburg', 'Kathmandu',
    'Kigali', 'Kraków', 'Kuala Lumpur', 'Kyoto', 'La Paz', 'Lagos', 'Las Vegas', 'Lima', 'Lisbon', 'Ljubljana',
    'London', 'Los Angeles', 'Lucerne', 'Luxembourg City', 'Lyon', 'Madrid', 'Malaga', 'Manama', 'Manila', 'Marrakech',
    'Marseille', 'Mendoza', 'Mexico City', 'Miami', 'Milan', 'Montevideo', 'Montreal', 'Moscow', 'Munich', 'Muscat',
    'Nairobi', 'Naples', 'New York', 'Nice', 'Panama City', 'Paris', 'Pattaya', 'Phnom Penh', 'Phuket', 'Porto',
    'Porto Alegre', 'Prague', 'Punta Arenas', 'Quebec City', 'Quito', 'Recife', 'Reykjavik', 'Rio de Janeiro', 'Rome',
    'Salvador', 'San Francisco', 'San José', 'Santiago', 'Seoul', 'Seville', 'Shanghai', 'Singapore', 'Split',
    'Stockholm', 'Sydney', 'Tbilisi', 'Tel Aviv', 'Thimphu', 'Tokyo', 'Toronto', 'Tunis', 'Ulaanbaatar', 'Valparaíso',
    'Vancouver', 'Venice', 'Victoria', 'Vienna', 'Warsaw', 'Yogyakarta', 'Zanzibar City', 'Zurich'
]

# Iterate over the cities and process each one
for city in cities_to_process:
    calculate_distance_and_insert(city)
