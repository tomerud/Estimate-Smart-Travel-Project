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


def generate_vectors(city_name, budget_style, month):
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Fetch all cities from the `top_touristic_cities` table
        cursor.execute("SELECT city FROM top_touristic_cities WHERE city != %s", (city_name,))
        all_cities = cursor.fetchall()

        if not all_cities:
            raise ValueError("No other cities found in the database.")

        print(f"\nGenerating vectors for {city_name} with budget style '{budget_style}' for the month of {month}...")

        for city in all_cities:
            other_city = city["city"]

            try:
                # Generate vector for the current city compared to the base city
                vector = get_city_vector(other_city, budget_style, month, city_name)
                print(f"Vector for {city_name} compared to {other_city}: {vector}")
            except Exception as e:
                print(f"Error generating vector for {other_city}: {e}")

    finally:
        cursor.close()
        db.close()


# Example Usage
print("\nGenerating vectors for a base city...")
generate_vectors("Amsterdam", "budget", "January")
