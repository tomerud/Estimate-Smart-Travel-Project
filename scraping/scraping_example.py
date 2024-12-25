import requests
from bs4 import BeautifulSoup
import json

# URL for one city (Athens) to illustrate the process
url = 'https://www.holiday-weather.com/eilat/averages/'


def scrape_city_temperatures(url):
    # Step 1: Fetch the page content
    response = requests.get(url)
    print("Fetched page content")  # Print statement to track the request

    # Step 2: Check if the request was successful
    if response.status_code == 200:
        print("Request successful, status code:", response.status_code)

        # Step 3: Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Parsed HTML content with BeautifulSoup")  # Indicate parsing is done

        # Step 4: Find the div element with the 'data-chart' attribute
        chart_div = soup.find("div", {"data-chart": True})
        print("Located chart div:", chart_div)  # Print the entire div for inspection

        # Step 5: Check if the 'data-chart' attribute is present and parse it
        if chart_div:
            chart_data = chart_div["data-chart"]
            print("Extracted data-chart attribute:", chart_data)  # Shows raw JSON data as a string

            # Step 6: Parse the JSON string in data-chart
            chart_data = json.loads(chart_data)  # Convert JSON string to Python dictionary
            print("Parsed data-chart as JSON:", chart_data)  # Inspect the parsed JSON structure

            # Step 7: Locate the series with the temperature data (look for "Centigrade")
            for series in chart_data["series"]:
                print("Inspecting series:", series)  # Print each series entry
                if series["name"] == "Centigrade":
                    temperatures = series["data"]
                    print("Extracted temperatures:", temperatures)  # Final temperatures for each month
                    return temperatures
        else:
            print("Temperature data not found.")
    else:
        print("Request failed, status code:", response.status_code)


# Run the function for one city to see detailed output
scrape_city_temperatures(url)
