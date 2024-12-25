from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import plotly.express as px
import os

# Load environment variables from .env file
load_dotenv()

def fetch_all_locations():
    # Connect to the MySQL database using environment variables
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 3306)),  # Use default port if not set
        database=os.getenv("DB_NAME")
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


def create_informative_map(locations_df):
    # Create an interactive scatter plot map with Plotly
    fig = px.scatter_geo(
        locations_df,
        lat='latitude',
        lon='longitude',
        hover_name='city',
        hover_data={
            "country": True,  # Add country to the hover data
            "human_development_index": True,
            "religion": True,
            "language": True,
            "latitude": False,  # Hide in hover data
            "longitude": False  # Hide in hover data
        },
        title="Interactive Map of All Touristic Locations by City",
    )

    # Customize marker size, color, and opacity
    fig.update_traces(marker=dict(size=5, color="blue", opacity=0.7))  # Smaller and more subtle markers

    # Use a minimalistic map style
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="whitesmoke",
        oceancolor="lightblue",
        showocean=True,
        showlakes=False,
        showcountries=True,
        countrycolor="lightgray",
        coastlinecolor="lightgray"
    )

    # Update layout for a minimalistic look
    fig.update_layout(
        title="Interactive Map of All Touristic Locations by City",
        font=dict(size=12),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        showlegend=False
    )

    # Display the map
    fig.show()


def main():
    # Fetch all location data from the database
    locations_df = fetch_all_locations()

    if locations_df is not None:
        # Create and display the informative map
        create_informative_map(locations_df)


if __name__ == "__main__":
    main()
