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

    # Fetch a list of 50 cities
    cursor.execute("SELECT * FROM cities LIMIT 51")
    cities = cursor.fetchall()

    if not cities:
        print("No cities found in the database.")
        return

    # Display the city list for user selection
    print("Choose a city from the following list:")
    for i, city in enumerate(cities):
        print(f"{i + 1}. {city['City']}")  # Using the exact column name 'City'

    # Get user input
    chosen_index = int(input("Enter the number corresponding to your chosen city: ")) - 1
    if chosen_index < 0 or chosen_index >= len(cities):
        print("Invalid choice. Please try again.")
        return None

    # Get the chosen city data
    input_city_data = cities[chosen_index]
    print(f"Chosen city: {input_city_data['City']}")  # Using the exact column name 'City'

    # Initialize variables for finding the most similar city
    most_similar_city = None
    smallest_distance = float('inf')

    # Compare the chosen city with the other 49 cities
    for city in cities:
        if city["City"] == input_city_data["City"]:  # Using 'City' to check for the chosen city
            continue  # Skip the chosen city itself

        # Parse latitude and longitude from the Location string format
        loc1 = tuple(map(float, input_city_data["Location"].split(',')))
        loc2 = tuple(map(float, city["Location"].split(',')))

        # Calculate similarity based on location
        location_distance = geodesic(loc1, loc2).kilometers

        # Calculate similarity on HDI, religion, and language
        hdi_difference = abs(input_city_data["Development Ranking (HDI)"] - city[
            "Development Ranking (HDI)"])  # Using the exact column name
        religion_similarity = int(input_city_data["Religion"] == city["Religion"])
        language_similarity = int(input_city_data["Language"] == city["Language"])

        # Compute a weighted similarity score
        total_similarity = location_distance * 0.3 + hdi_difference * 0.4
        total_similarity -= religion_similarity * 0.15
        total_similarity -= language_similarity * 0.15

        # Track the most similar city
        if total_similarity < smallest_distance:
            smallest_distance = total_similarity
            most_similar_city = city

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Return the most similar city
    if most_similar_city:
        print(f"The most similar city to {input_city_data['City']} is {most_similar_city['City']}.")  # Using 'City'
    return most_similar_city


# Call the function to run it
get_most_similar_city()
