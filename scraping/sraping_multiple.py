import requests
from bs4 import BeautifulSoup
import time


# Function to get daily costs for different travel styles
def get_daily_costs(geonameid):
    # Base URL template with placeholders for geonameid and budgettype
    url_template = "https://www.budgetyourtrip.com/budgetreportadv.php?geonameid={}&countrysearch=&country_code=&categoryid=0&budgettype={}&triptype=0&startdate=&enddate=&travelerno=0"

    # Travel style mappings
    travel_styles = {
        'budget': 1,
        'midrange': 2,
        'luxury': 3
    }

    # Dictionary to store costs for each travel style
    costs = {}

    # Loop over each travel style and scrape the respective page
    for style, budgettype in travel_styles.items():
        # Create the specific URL for each travel style
        city_url = url_template.format(geonameid, budgettype)

        # Send GET request to the city's URL
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        response = requests.get(city_url, headers=headers)
        response.raise_for_status()  # Check for request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate and retrieve the daily cost for the current travel style
        cost_element = soup.find("span", class_="curvalue")
        if cost_element:
            costs[style] = cost_element.get_text(strip=True)
        else:
            print(f"Unable to find cost value for {style} travel style.")

    return costs


# List of cities with their corresponding geonameid values
cities = {
    "Abu Dhabi": 292968,
    "Accra": 2306104,
    "Almaty": 1526384,
    "Amman": 250441,
    "Amsterdam": 2759794,
    "Antofagasta": 3899539,
    "Antwerp": 2803138,
    "Arequipa": 3947322,
    "Asmara": 343300,
    "Asunción": 3439389,
    "Athens": 264371,
    "Auckland": 2193733,
    "Baku": 587084,
    "Bangalore": 1277333,
    "Bangkok": 1609350,
    "Barcelona": 3128760,
    "Basel": 2661604,
    "Beijing": 1816670,
    "Beirut": 276781,
    "Belgrade": 792680,
    "Bergen": 3161732,
    "Berlin": 2950159,
    "Bogotá": 3688689,
    "Bologna": 3181928,
    "Brasilia": 3469058,
    "Bratislava": 3060972,
    "Brussels": 2800866,
    "Budapest": 3054643,
    "Buenos Aires": 3435910
}

# Dictionary to store costs for each city
all_city_costs = {}

# Loop through each city and get daily costs
for city_name, geonameid in cities.items():
    print(f"Fetching data for {city_name}...")
    city_costs = get_daily_costs(geonameid)
    all_city_costs[city_name] = city_costs
    time.sleep(1)  # Sleep to prevent overwhelming the server

# Display the collected data
for city, costs in all_city_costs.items():
    print(f"{city}: {costs}")
