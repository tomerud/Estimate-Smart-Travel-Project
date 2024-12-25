import requests
from bs4 import BeautifulSoup
import json

def scrape_city_temperatures(url):
    # Send a GET request to fetch the page content
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the element containing the data-chart attribute
    chart_div = soup.find("div", {"data-chart": True})
    if chart_div:
        # Extract the JSON data from the data-chart attribute
        chart_data = json.loads(chart_div["data-chart"])

        # Extract temperatures from the JSON data under "series"
        for series in chart_data["series"]:
            if series["name"] == "Centigrade":  # Adjust if needed
                temperatures = series["data"]
                print("Extracted temperatures:", temperatures)
                return temperatures
    else:
        print("Temperature data not found.")

# Example usage for Athens
scrape_city_temperatures("https://www.holiday-weather.com/athens/averages/")
