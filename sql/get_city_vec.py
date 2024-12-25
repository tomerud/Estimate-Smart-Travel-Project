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


# Function to generate the city vector with norm_dist for a second city
def get_city_vector(city_name, budget_style, month, second_city):
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Corrected column name for monthly temperature normalization
        month_column = f"{month.lower()}_avg_temp_norm"

        # Fetch vector components from normalized_data
        query = f"""
            SELECT
                nd.city_id,
                nd.human_dev_ranking,
                nd.is_christian,
                nd.is_muslim,
                nd.is_hindu,
                nd.is_buddhist,
                nd.is_shinto,
                nd.is_jewish,
                nd.is_english,
                nd.is_french,
                nd.is_german,
                nd.is_arabic,
                nd.is_spanish,
                nd.is_slavic,
                nd.is_other_european,
                nd.is_asian,
                nd.is_african,
                nd.{budget_style}_price_norm AS normalized_price,
                nd.is_party_city,
                nd.is_beach_city,
                nd.{month_column} AS normalized_temp
            FROM top_touristic_cities AS ttc
            INNER JOIN normalized_data AS nd ON ttc.city_id = nd.city_id
            WHERE ttc.city = %s;
        """
        cursor.execute(query, (city_name,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"City '{city_name}' not found.")

        # Fetch normalized distance for the second city
        distance_table = "distance_from_" + city_name.replace(" ", "_").lower()

        cursor.execute("""
            SELECT ttc.city_id
            FROM top_touristic_cities AS ttc
            WHERE ttc.city = %s
        """, (second_city,))
        second_city_data = cursor.fetchone()

        if not second_city_data:
            raise ValueError(f"Second city '{second_city}' not found.")

        second_city_id = second_city_data["city_id"]

        cursor.execute(f"""
            SELECT norm_dist
            FROM {distance_table}
            WHERE dest_id = %s
        """, (second_city_id,))
        norm_dist_data = cursor.fetchone()

        norm_dist = float(norm_dist_data["norm_dist"]) if norm_dist_data else 0.0

        # Print explanation of vector entries
        # print("\nVector entries explanation:")
        # print("[city_id, human_dev_ranking, is_christian, is_muslim, is_hindu, is_buddhist, "
        #       "is_shinto, is_jewish, is_english, is_french, is_german, is_arabic, is_spanish, "
        #       "is_slavic, is_other_european, is_asian, is_african, normalized_price, "
        #       "is_party_city, is_beach_city, normalized_temp, norm_dist_to_second_city]")

        # Construct the vector
        vector = [
            result["city_id"],
            result["human_dev_ranking"],
            result["is_christian"],
            result["is_muslim"],
            result["is_hindu"],
            result["is_buddhist"],
            result["is_shinto"],
            result["is_jewish"],
            result["is_english"],
            result["is_french"],
            result["is_german"],
            result["is_arabic"],
            result["is_spanish"],
            result["is_slavic"],
            result["is_other_european"],
            result["is_asian"],
            result["is_african"],
            result["normalized_price"],
            result["is_party_city"],
            result["is_beach_city"],
            result["normalized_temp"],  # Include normalized temperature for the given month
            norm_dist  # Add norm_dist to the vector
        ]

        # Print the constructed vector
        # print(f"Vector for {city_name} including norm_dist to {second_city}: {vector}")
        return vector

    finally:
        cursor.close()
        db.close()


# Run Example
# if __name__ == "__main__":
#     print("\nExample: Generating a vector...")
#     city_name = "moscow"  # Base city
#     budget_style = "budget"  # Budget style (e.g., budget, midrange, luxury)
#     month = "January"        # Month to include temperature normalization
#     second_city = "Sydney"   # Target city to calculate norm_dist
#
#     # Get the vector for Amsterdam compared to Sydney
#     try:
#         vector = get_city_vector(city_name, budget_style, month, second_city)
#
#         # Use the returned vector for further processing or analysis
#         print(f"\nReturned vector: {vector}")
#     except ValueError as e:
#         print(f"Error: {e}")
#     except mysql.connector.Error as db_err:
#         print(f"Database Error: {db_err}")
