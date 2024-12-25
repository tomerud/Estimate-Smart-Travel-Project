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


def create_city_vector(city_name):
    # Initialize the vector
    city_vector = []

    # List of tables to check with their column names
    tables = {
        "airports": ["iata_code", "airport_name", "municipality", "longitude", "latitude", "municipality"],
        # 'municipality' is the city column
        "beach_cities": ["city_name"],  # 'city_name' is the city column
        "party_cities": ["city"],  # 'city' is the city column
        "tel_aviv_flights": ["destination", "airport_code", "january_avg_price", "february_avg_price",
                             "march_avg_price", "april_avg_price",
                             "may_avg_price", "june_avg_price", "july_avg_price", "august_avg_price",
                             "september_avg_price",
                             "october_avg_price", "november_avg_price", "december_avg_price"],
        # 'destination' may refer to city
        "top_touristic_cities": ["city", "country", "continent", "language", "religion", "human_development_index",
                                 "latitude", "longitude", "budget_price_usd", "midrange_price_usd", "luxury_price_usd"],
        # 'city' is the city column
        "weather": ["city", "january_avg_temp", "february_avg_temp", "march_avg_temp", "april_avg_temp", "may_avg_temp",
                    "june_avg_temp", "july_avg_temp", "august_avg_temp", "september_avg_temp", "october_avg_temp",
                    "november_avg_temp", "december_avg_temp"]  # 'city' is the city column
    }

    # Loop through each table and check if the city exists
    for table, columns in tables.items():
        city_column = [col for col in columns if
                       "city" in col.lower()]  # Try to identify the column that stores city names

        if not city_column:
            print(f"Error: No 'city' column found for table {table}")
            continue  # Skip this table if no 'city' column is found

        # SQL query to check if the city exists in the current table
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {city_column[0]} = %s", (city_name,))
        city_exists = cursor.fetchone()[0] > 0  # If count > 0, the city exists in the table

        # Add 1 if city exists, else add 0
        if city_exists:
            city_vector.append(1)
        else:
            city_vector.append(0)

    # Return the vector
    return city_vector


# Example usage
city_name = "Amsterdam"  # You can change this to any city you're interested in
vector = create_city_vector(city_name)

# Output the vector
print(f"Vector for city '{city_name}': {vector}")

# Close the cursor and connection
cursor.close()
conn.close()
