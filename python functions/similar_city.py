import mysql.connector
from geopy.distance import geodesic


def get_most_similar_city():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="112145",
        port=3306,
        database="cities"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch all cities from the table
    cursor.execute("SELECT * FROM top_touristic_cities")
    cities = cursor.fetchall()

    if not cities:
        print("No cities found in the database.")
        return None

    # Display the city list for user selection
    print("Choose a city from the following list:")
    for i, city in enumerate(cities):
        print(f"{i + 1}. {city['city']}")  # Using the exact column name 'city'

    # Get user input
    try:
        chosen_index = int(input("Enter the number corresponding to your chosen city: ")) - 1
        if chosen_index < 0 or chosen_index >= len(cities):
            print("Invalid choice. Please try again.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

    # Get the chosen city data
    input_city_data = cities[chosen_index]
    print(f"Chosen city: {input_city_data['city']}")

    # Initialize variables for finding the most similar city
    most_similar_city = None
    smallest_similarity_score = float('inf')

    # Compare the chosen city with each other city
    for city in cities:
        if city["city"] == input_city_data["city"]:  # Skip the chosen city itself
            continue

        # Get the coordinates for distance calculation
        loc1 = (input_city_data["latitude"], input_city_data["longitude"])
        loc2 = (city["latitude"], city["longitude"])

        # Calculate geographic distance
        location_distance = geodesic(loc1, loc2).kilometers

        # Calculate HDI difference
        hdi_difference = abs(input_city_data["human_development_index"] - city["human_development_index"])

        # Check for religion and language similarity
        religion_similarity = int(input_city_data["religion"] == city["religion"])
        language_similarity = int(input_city_data["language"] == city["language"])

        # Compute a weighted similarity score
        similarity_score = location_distance * 0.3 + hdi_difference * 0.4
        similarity_score -= religion_similarity * 0.15
        similarity_score -= language_similarity * 0.15

        # Track the most similar city
        if similarity_score < smallest_similarity_score:
            smallest_similarity_score = similarity_score
            most_similar_city = city

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Return the most similar city
    if most_similar_city:
        print(f"The most similar city to {input_city_data['city']} is {most_similar_city['city']}.")
    else:
        print("Could not find a similar city.")

    return most_similar_city


# Call the function to run it
get_most_similar_city()
