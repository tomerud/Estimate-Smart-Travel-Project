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

# List of airport data to be inserted into the 'airports' table
airports_data = [
    ("AQP", "Alfredo Rodríguez Ballón International Airport", "Arequipa", -16.341100, -71.572800),
    ("ATH", "Eleftherios Venizelos International Airport", "Athens", 37.936400, 23.948400),
    ("BRU", "Brussels Airport", "Brussels", 50.901000, 4.484400),
    ("CDG", "Charles de Gaulle Airport", "Paris", 49.009700, 2.552200),
    ("CTG", "Rafael Núñez International Airport", "Cartagena", 10.442600, -75.513000),
    ("DEL", "Indira Gandhi International Airport", "Delhi", 28.556200, 77.099900),
    ("HAN", "Noi Bai International Airport", "Hanoi", 21.221200, 105.801900),
    ("IST", "Istanbul Airport", "Istanbul", 41.275300, 28.814600),
    ("KIX", "Kansai International Airport", "Kyoto", 34.434700, 135.244700),
    ("KRK", "John Paul II International Airport", "Krakow", 50.077700, 19.784800),
    ("KUL", "Kuala Lumpur International Airport", "Kuala Lumpur", 2.745600, 101.709900),
    ("LJU", "Ljubljana Jože Pučnik Airport", "Ljubljana", 46.223700, 14.457600),
    ("LPB", "El Alto International Airport", "La Paz", -16.513300, -68.177100),
    ("MNL", "Ninoy Aquino International Airport", "Manila", 14.508600, 121.019600),
    ("MRS", "Marseille Provence Airport", "Marseille", 43.436700, 5.221400),
    ("MXP", "Milan Malpensa Airport", "Milan", 45.630000, 8.711400),
    ("NAP", "Naples International Airport", "Naples", 40.883300, 14.290600),
    ("PTY", "Tocumen International Airport", "Panama City", 9.071400, -79.383500),
    ("VCE", "Venice Marco Polo Airport", "Venice", 45.505300, 12.351900),
    ("ZNZ", "Abeid Amani Karume International Airport", "Zanzibar City", -6.222000, 39.224600)
]

# SQL query to insert or update the airport name for existing IATA codes
insert_airport_query = """
INSERT INTO airports (iata_code, airport_name, municipality, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    airport_name = VALUES(airport_name);
"""

# Insert each airport's data into the 'airports' table
for airport in airports_data:
    cursor.execute(insert_airport_query, airport)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Airport data inserted or updated in the 'airports' table successfully.")
