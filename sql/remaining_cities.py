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

# SQL query to find cities in top_touristic_cities that are not in weather
query = """
SELECT t.city 
FROM top_touristic_cities t
LEFT JOIN weather w ON t.city = w.city
WHERE w.city IS NULL;
"""

# Execute the query
cursor.execute(query)

# Fetch and display the results
missing_cities = cursor.fetchall()
print("Cities in `top_touristic_cities` but not in `weather` table:")
for city in missing_cities:
    print(city[0])

# Close the cursor and connection
cursor.close()
conn.close()
