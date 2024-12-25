import mysql.connector
import dotenv
import os
from get_city_vec import get_city_vector

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


# Function to generate vectors for all cities compared to a given city
def generate_all_vectors(city_name, budget_style, month):
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Fetch all cities except the base city
        cursor.execute("SELECT city FROM top_touristic_cities")
        all_cities = cursor.fetchall()

        if not all_cities:
            raise ValueError("No other cities found in the database.")

        vectors = []

        # print(f"\nGenerating vectors for all cities compared to {city_name}...")

        # Iterate over each city and generate the vector
        for city in all_cities:
            other_city = city["city"]
            try:
                # Call the `get_city_vector` function with swapped arguments
                vector = get_city_vector(other_city, budget_style, month, city_name)
                vectors.append(vector)
                # print(f"Vector for {other_city} compared to {city_name}: {vector}")
            except Exception as e:
                print(f"Error generating vector for {other_city}: {e}")

        return vectors

    finally:
        cursor.close()
        db.close()


# Example Usage
# if __name__ == "__main__":
#     print("\nExample: Generating vectors for all cities compared to a given city...")
#     city_name = "Amsterdam"  # City to compare against
#     budget_style = "budget"  # Budget style (e.g., budget, midrange, luxury)
#     month = "January"        # Month (currently unused but included for extension)
#
#     # Generate all vectors
#     vectors = generate_all_vectors(city_name, budget_style, month)
#
#     # Print the results
#     print("\nAll generated vectors:")
#     for vector in vectors:
#         print(vector)
