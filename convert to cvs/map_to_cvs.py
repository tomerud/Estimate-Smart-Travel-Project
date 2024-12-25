import mysql.connector
import pandas as pd

def fetch_all_locations():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="112145",
        port=3306,
        database="cities"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch city data with adjusted column names
    cursor.execute("SELECT city, country, human_development_index, religion, language, latitude, longitude FROM top_touristic_cities")
    locations = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Check if we have data
    if not locations:
        print("No location data found.")
        return None

    # Convert to a DataFrame for easy manipulation
    locations_df = pd.DataFrame(locations)

    return locations_df

def save_data_to_csv():
    # Fetch data from MySQL
    locations_df = fetch_all_locations()

    # Save the DataFrame to CSV
    if locations_df is not None:
        locations_df.to_csv("touristic_locations.csv", index=False)
        print("Data saved to 'touristic_locations.csv'.")

# Call the function to save the data
save_data_to_csv()
