from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables from .env file
load_dotenv()

# Sample data to insert
cities_data = [
    ("Hanoi", "Vietnam", "Asia", "Vietnamese", "Buddhism", 0.694, 21.0285, 105.8542),
    ("Ho Chi Minh City", "Vietnam", "Asia", "Vietnamese", "Buddhism", 0.694, 10.8231, 106.6297),
    ("Chennai", "India", "Asia", "Tamil", "Hinduism", 0.645, 13.0827, 80.2707),
    ("Bangalore", "India", "Asia", "Kannada", "Hinduism", 0.645, 12.9716, 77.5946),
    ("Abu Dhabi", "UAE", "Asia", "Arabic", "Islam", 0.890, 24.4539, 54.3773),
    ("Doha", "Qatar", "Asia", "Arabic", "Islam", 0.848, 25.276987, 51.521008),
    ("Haifa", "Israel", "Asia", "Hebrew", "Judaism", 0.919, 32.7940, 34.9896),
    ("Victoria", "Seychelles", "Africa", "English/French", "Christianity", 0.796, -4.6191, 55.4513),
    ("Libreville", "Gabon", "Africa", "French", "Christianity", 0.703, 0.4162, 9.4673),
    ("Maputo", "Mozambique", "Africa", "Portuguese", "Christianity", 0.456, -25.9692, 32.5732),
    ("Luanda", "Angola", "Africa", "Portuguese", "Christianity", 0.581, -8.8390, 13.2894),
    ("Asmara", "Eritrea", "Africa", "Tigrinya", "Christianity/Islam", 0.459, 15.3229, 38.9251),
    ("Port Louis", "Mauritius", "Africa", "English/French", "Hinduism/Christianity", 0.802, -20.1609, 57.5012),
    ("Porto Alegre", "Brazil", "South America", "Portuguese", "Christianity", 0.754, -30.0346, -51.2177),
    ("Recife", "Brazil", "South America", "Portuguese", "Christianity", 0.754, -8.0476, -34.8770),
    ("Guayaquil", "Ecuador", "South America", "Spanish", "Christianity", 0.759, -2.1708, -79.9224),
    ("Maracaibo", "Venezuela", "South America", "Spanish", "Christianity", 0.711, 10.6666, -71.6125),
    ("Eilat", "Israel", "Asia", "Hebrew", "Judaism", 0.919, 29.5577, 34.9519),
    ("Punta Arenas", "Chile", "South America", "Spanish", "Christianity", 0.851, -53.1638, -70.9171),
    ("Antofagasta", "Chile", "South America", "Spanish", "Christianity", 0.851, -23.6509, -70.3975)
]

# Connect to MySQL database using environment variables
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", 3306)),  # Use 3306 as the default if DB_PORT is not set
    database=os.getenv("DB_NAME")
)

# Create a cursor object
cursor = conn.cursor()

# SQL query to insert data, ignoring duplicates
insert_query = """
INSERT IGNORE INTO top_touristic_cities (city, country, continent, language, religion, human_development_index, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

# Insert each row of data into the table
cursor.executemany(insert_query, cities_data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data inserted successfully into 'top_touristic_cities' table.")
