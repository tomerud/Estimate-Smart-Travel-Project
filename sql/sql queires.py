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
    port=int(os.getenv("DB_PORT", 3306)),  # Use 3306 as default if not set
    database=os.getenv("DB_NAME")
)

# Create a cursor
cursor = conn.cursor()

def top_10_cities_by_hdi():
    query = """
    SELECT city, country, continent, human_development_index
    FROM top_touristic_cities
    ORDER BY human_development_index DESC
    LIMIT 10;
    """
    cursor.execute(query)
    return cursor.fetchall()

def count_cities_by_continent():
    query = """
    SELECT continent, COUNT(*) AS number_of_cities
    FROM top_touristic_cities
    GROUP BY continent
    ORDER BY number_of_cities DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()

def total_number_of_cities():
    query = """
    SELECT COUNT(*) AS total_number_of_cities
    FROM top_touristic_cities;
    """
    cursor.execute(query)
    return cursor.fetchone()[0]

# Call functions and print results
print("Top 10 Cities by HDI:")
for row in top_10_cities_by_hdi():
    print(row)

print("\nNumber of Cities by Continent:")
for row in count_cities_by_continent():
    print(row)

print("\nTotal Number of Cities:")
print(total_number_of_cities())

# Close the cursor and connection
cursor.close()
conn.close()
