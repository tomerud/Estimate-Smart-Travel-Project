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

# Define the query to retrieve July temperatures for all cities in Italy
query = """
SELECT w.city, w.july_avg_temp
FROM weather w
JOIN top_touristic_cities t ON w.city = t.city
WHERE t.country = 'Italy';
"""

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
print("Average July Temperatures for Cities in Italy:")
for city, temp in results:
    print(f"{city}: {temp}°C")

# Close the cursor and connection
cursor.close()
conn.close()
