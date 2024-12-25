import numpy as np
from city_similarity import generate_all_vectors, get_city_vector
import mysql.connector
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


def get_city_name_by_id(city_id):
    """
    Fetches the city name corresponding to a given city_id.

    Args:
        city_id (int): The city_id to fetch the name for.

    Returns:
        str: The city name.
    """
    db = connect_db()
    cursor = db.cursor()

    try:
        query = "SELECT city FROM top_touristic_cities WHERE city_id = %s"
        cursor.execute(query, (city_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        cursor.close()
        db.close()


def calculate_similarity(city_name, budget_style, month):
    """
    Calculates the Euclidean distance between the city vector for a city to itself
    and all other city vectors, excluding city_id from the calculation.

    Args:
        city_name (str): The name of the base city for comparison.
        budget_style (str): The budget style (e.g., budget, midrange, luxury).
        month (str): The month (currently unused, included for extension).

    Returns:
        None: Prints the similarity rankings in decreasing order of similarity (shorter distance).
    """
    # Generate the vector for the city compared to itself
    base_vector = get_city_vector(city_name, budget_style, month, city_name)

    # Handle None values in base_vector and remove city_id for distance calculations
    base_vector_trimmed = np.array([x if x is not None else 0 for x in base_vector[1:]])

    # Generate vectors for all other cities compared to the base city
    all_vectors = generate_all_vectors(city_name, budget_style, month)

    # Calculate Euclidean distances
    distances = []
    for vector in all_vectors:
        other_city_id = vector[0]  # The city_id of the current city
        other_vector_trimmed = np.array([x if x is not None else 0 for x in vector[1:]])  # Exclude city_id and handle None
        distance = np.linalg.norm(base_vector_trimmed - other_vector_trimmed)  # Euclidean distance
        other_city_name = get_city_name_by_id(other_city_id)  # Fetch the city name using city_id
        distances.append((other_city_name, distance))

    # Sort distances in increasing order (closer means more similar)
    distances.sort(key=lambda x: x[1])

    # Print similarity rankings
    print(f"\nSimilarity rankings for {city_name}:")
    print(f"{'City':<20} {'Distance':<10}")
    print("-" * 30)

    for city, distance in distances:
        print(f"{city:<20} {distance:<10.5f}")


# Example Usage
if __name__ == "__main__":
    city_name = "Tel Aviv"  # Base city for comparison
    budget_style = "midrange"  # Budget style (e.g., budget, midrange, luxury)
    month = "June"        # Month (currently unused)

    calculate_similarity(city_name, budget_style, month)
