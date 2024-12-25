import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MySQL database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Define airport data to insert into the airports table
airport_data = [
    ("VCE", "Venice", 12.3519, 45.5053),        # Venice Marco Polo Airport
    ("BRU", "Brussels", 4.4844, 50.9010),       # Brussels Airport
    ("MXP", "Milan", 8.7114, 45.6300),          # Milan Malpensa Airport
    ("NAP", "Naples", 14.2906, 40.8833),        # Naples International Airport
    ("KRK", "Krakow", 19.7848, 50.0777),        # Krakow John Paul II International
    ("LJU", "Ljubljana", 14.4576, 46.2237),     # Ljubljana Jože Pučnik Airport
    ("AQP", "Arequipa", -71.5728, -16.3411),    # Rodríguez Ballón International Airport
    ("KUL", "Kuala Lumpur", 101.7099, 2.7456),  # Kuala Lumpur International Airport
    ("MRS", "Marseille", 5.2214, 43.4367),      # Marseille Provence Airport
    ("CDG", "Paris", 2.5522, 49.0097),          # Charles de Gaulle Airport
    ("KIX", "Kyoto", 135.2447, 34.4347),        # Kansai International (serves Kyoto)
    ("LPB", "La Paz", -68.1771, -16.5133),      # El Alto International Airport
    ("ZNZ", "Zanzibar City", 39.2246, -6.2220), # Abeid Amani Karume International
    ("CTG", "Cartagena", -75.5130, 10.4426),    # Rafael Núñez International Airport
    ("PTY", "Panama City", -79.3835, 9.0714),   # Tocumen International Airport
    ("HAN", "Hanoi", 105.8019, 21.2212),        # Noi Bai International Airport
    ("ATH", "Athens", 23.9484, 37.9364),        # Athens International Airport
    ("DEL", "Delhi", 77.0999, 28.5562),         # Indira Gandhi International Airport
    ("IST", "Istanbul", 28.8146, 41.2753),      # Istanbul Airport
    ("MNL", "Manila", 121.0196, 14.5086)        # Ninoy Aquino International Airport
]

# SQL query to insert data into the airports table
insert_query = """
INSERT INTO airports (iata_code, municipality, longitude, latitude)
VALUES (%s, %s, %s, %s);
"""

# Execute the insertion for each airport in the list
for airport in airport_data:
    cursor.execute(insert_query, airport)

# Commit the changes
conn.commit()
print("Airports added successfully to the airports table.")

# Close the cursor and connection
cursor.close()
conn.close()
