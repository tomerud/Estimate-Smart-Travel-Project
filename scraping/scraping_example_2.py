import requests
from bs4 import BeautifulSoup
import json

# URL for one city (Eilat) to illustrate the process
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

        # Print the full HTML to see if what we looking for there
       # print(soup.prettify())
        #from here try figure out what to find
        temperature_div = soup.find('div', {'id': 'temperature', 'data-chart': True})

        # Check if the div was found
        if temperature_div:
            # Print the 'data-chart' attribute content
            print(temperature_div['data-chart'])
        else:
            print("Temperature data not found.")

        #converting to dictionary

        data_chart = temperature_div['data-chart']
        data_dict = json.loads(data_chart)  # Parse JSON-like string into dictionary
        print(data_dict)
        series = data_dict['series']
        print( "series:", series)
        centigrade_data = series[0]
        print(centigrade_data)




scrape_city_temperatures(url)
