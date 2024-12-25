import requests
from bs4 import BeautifulSoup


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


# Example usage with the provided geonameid for Bangkok
geonameid = 1609350
city_costs = get_daily_costs(geonameid)
print(city_costs)
