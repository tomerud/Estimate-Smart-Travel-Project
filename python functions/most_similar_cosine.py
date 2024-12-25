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


def cosine_similarity(vector1, vector2):
    """
    Calculates cosine similarity between two vectors.

    Args:
        vector1 (np.array): First vector.
        vector2 (np.array): Second vector.

    Returns:
        float: Cosine similarity between the vectors.
    """
    dot_product = np.dot(vector1, vector2)
    norm_v1 = np.linalg.norm(vector1)
    norm_v2 = np.linalg.norm(vector2)
    return dot_product / (norm_v1 * norm_v2)


def calculate_similarity(city_name, budget_style, month):
    """
    Calculates the Cosine Similarity between the city vector for a city to itself
    and all other city vectors, excluding city_id from the calculation.

    Args:
        city_name (str): The name of the base city for comparison.
        budget_style (str): The budget style (e.g., budget, midrange, luxury).
        month (str): The month (currently unused, included for extension).

    Returns:
        None: Prints the similarity rankings in decreasing order of similarity.
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

    # Handle None values in base_vector and remove city_id for similarity calculations
    base_vector_trimmed = np.array([x if x is not None else 0 for x in base_vector[1:]])

    # Generate vectors for all other cities compared to the base city
    all_vectors = generate_all_vectors(city_name, budget_style, month)

    # Calculate Cosine Similarities
    similarities = []
    city_vectors = {}  # Dictionary to store vectors for each city
    for vector in all_vectors:
        other_city_id = vector[0]  # The city_id of the current city
        other_vector_trimmed = np.array([x if x is not None else 0 for x in vector[1:]])  # Exclude city_id and handle None
        similarity = cosine_similarity(base_vector_trimmed, other_vector_trimmed)  # Cosine similarity
        other_city_name = get_city_name_by_id(other_city_id)  # Fetch the city name using city_id
        similarities.append((other_city_name, similarity))
        city_vectors[other_city_name] = other_vector_trimmed  # Store the vector

    # Sort similarities in decreasing order (higher means more similar)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Print similarity rankings
    print(f"\nSimilarity rankings for {city_name}:")
    print(f"{'City':<20} {'Similarity':<10}")
    print("-" * 30)

    for city, similarity in similarities:
        print(f"{city:<20} {similarity:<10.5f}")

    # Print vectors for the top 3 similar cities with feature names
    print("\nVectors for the top 3 similar cities:")
    for i in range(min(3, len(similarities))):
        top_city = similarities[i][0]
        vector = city_vectors[top_city]
        print(f"\n{top_city}:")
        for idx, val in enumerate(vector):
            print(f"  {feature_names[idx + 1]}: {val:.5f}")  # Use feature name instead of generic feature label


# Example Usage
if __name__ == "__main__":
    city_name = "Barcelona"  # Base city for comparison
    budget_style = "luxury"  # Budget style (e.g., budget, midrange, luxury)
    month = "january"        # Month (currently unused)

    calculate_similarity(city_name, budget_style, month)
