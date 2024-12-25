import numpy as np
from city_similarity import generate_all_vectors, get_city_vector
import mysql.connector
import dotenv
import os
import time


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
def calculate_similarity(city_name, budget_style, month, weights=None):
    """
    Calculates the weighted Euclidean distance between the city vector for a city to itself
    and all other city vectors, excluding city_id from the calculation.

    Args:
        city_name (str): The name of the base city for comparison.
        budget_style (str): The budget style (e.g., budget, midrange, luxury).
        month (str): The month (currently unused, included for extension).
        weights (list or None): A list of weights for the features. If None, equal weight (1) is used.

    Returns:
        None: Prints the similarity rankings in decreasing order of similarity (shorter distance).
    """
    # Define feature names
    feature_names = [
        "city_id",
        "human_dev_ranking",
        "is_christian",
        "is_muslim",
        "is_hindu",
        "is_buddhist",
        "is_shinto",
        "is_jewish",
        "is_english",
        "is_french",
        "is_german",
        "is_arabic",
        "is_spanish",
        "is_slavic",
        "is_other_european",
        "is_asian",
        "is_african",
        "normalized_price",
        "is_party_city",
        "is_beach_city",
        "normalized_temp",
        "norm_dist"
    ]

    # Generate the vector for the city compared to itself
    base_vector = get_city_vector(city_name, budget_style, month, city_name)

    # Handle None values in base_vector and remove city_id for distance calculations
    base_vector_trimmed = np.array([x if x is not None else 0 for x in base_vector[1:]])

    # Default weights to 1 if not provided
    if weights is None:
        weights = np.ones_like(base_vector_trimmed)

    # Ensure weights are valid
    weights = np.array(weights)
    if len(weights) != len(base_vector_trimmed):
        raise ValueError("Weights vector length must match the number of features.")

    # Generate vectors for all other cities compared to the base city
    all_vectors = generate_all_vectors(city_name, budget_style, month)

    # Calculate weighted Euclidean distances
    distances = []
    city_vectors = {}  # Dictionary to store vectors for each city
    for vector in all_vectors:
        other_city_id = vector[0]  # The city_id of the current city
        other_vector_trimmed = np.array([x if x is not None else 0 for x in vector[1:]])  # Exclude city_id and handle None

        # Apply weights to the differences
        weighted_diff = weights * (base_vector_trimmed - other_vector_trimmed)
        distance = np.linalg.norm(weighted_diff)  # Weighted Euclidean distance

        other_city_name = get_city_name_by_id(other_city_id)  # Fetch the city name using city_id
        distances.append((other_city_name, distance))
        city_vectors[other_city_name] = other_vector_trimmed  # Store the vector

    # Sort distances in increasing order (closer means more similar)
    distances.sort(key=lambda x: x[1])

    # Print similarity rankings
    print(f"\nSimilarity rankings for {city_name}:")
    print(f"{'City':<20} {'Distance':<10}")
    print("-" * 30)

    for city, distance in distances:
        print(f"{city:<20} {distance:<10.5f}")

    # Print vectors for the top 3 similar cities with feature names
    print("\nVectors for the top 3 similar cities:")
    for i in range(min(3, len(distances))):
        top_city = distances[i][0]
        vector = city_vectors[top_city]
        print(f"\n{top_city}:")
        for idx, val in enumerate(vector):
            print(f"  {feature_names[idx + 1]}: {val:.5f}")  # Use feature name instead of generic feature label


# Example Usage
if __name__ == "__main__":
    city_name = "barcelona"  # Base city for comparison
    budget_style = "midrange"  # Budget style (e.g., budget, midrange, luxury)
    month = "march"  # Month

    # hum_dev_0, is_christ_1, is_muslim_2, is_hindu_3, is_buddhist_4, is_shinto_5,
    # is_jewish_6, is_english_7, is_french_8, is_german_9, is_arabic_10, is_spanish_11,
    # is_slavic_12, is_oth_euro_13, is_asian_14, is_african_15, norm_price_16, is_party_17,
    # is_beach_18, norm_temp_19, norm_dist_20

    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # Record start time
    start_time = time.time()
    calculate_similarity(city_name, budget_style, month, weights)

    # Record end time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"\nExecution time: {elapsed_time:.5f} seconds")

