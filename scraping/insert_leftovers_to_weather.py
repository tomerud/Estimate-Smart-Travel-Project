import requests
from bs4 import BeautifulSoup
import json
import mysql.connector
from dotenv import load_dotenv
import os
import time

# Load environment variables for MySQL connection
load_dotenv()

# Connect to MySQL database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Define the URLs for each city
city_urls = {
    'Amman': 'https://www.holiday-weather.com/amman/averages/',
    'Antwerp': 'https://www.holiday-weather.com/antwerp/averages/',
    'Arequipa': 'https://www.holiday-weather.com/arequipa/averages/',
    'Athens': 'https://www.holiday-weather.com/athens/averages/',
    'Bangalore': 'https://www.holiday-weather.com/bangalore/averages/',
    'Basel': 'https://www.holiday-weather.com/basel/averages/',
    'Bologna': 'https://www.holiday-weather.com/bologna/averages/',
    'Cartagena': 'https://www.holiday-weather.com/cartagena/averages/',
    'Casablanca': 'https://www.holiday-weather.com/casablanca/averages/',
    'Chengdu': 'https://www.holiday-weather.com/chengdu/averages/',
    'Chennai': 'https://www.holiday-weather.com/chennai/averages/',
    'Delhi': 'https://www.holiday-weather.com/delhi/averages/',
    'Doha': 'https://www.holiday-weather.com/doha/averages/',
    'Eilat': 'https://www.holiday-weather.com/eilat/averages/',
    'Fes': 'https://www.holiday-weather.com/fes/averages/',
    'Florence': 'https://www.holiday-weather.com/florence/averages/',
    'Geneva': 'https://www.holiday-weather.com/geneva/averages/',
    'Ghent': 'https://www.holiday-weather.com/ghent/averages/',
    'Hamburg': 'https://www.holiday-weather.com/hamburg/averages/',
    'Innsbruck': 'https://www.holiday-weather.com/innsbruck/averages/',
    'Jaipur': 'https://www.holiday-weather.com/jaipur/averages/',
    'Jerusalem': 'https://www.holiday-weather.com/jerusalem/averages/',
    'Kigali': 'https://www.holiday-weather.com/kigali/averages/',
    'Kraków': 'https://www.holiday-weather.com/krakow/averages/',
    'Lucerne': 'https://www.holiday-weather.com/lucerne/averages/',
    'Lyon': 'https://www.holiday-weather.com/lyon/averages/',
    'Malaga': 'https://www.holiday-weather.com/malaga/averages/',
    'Marrakech': 'https://www.holiday-weather.com/marrakech/averages/',
    'Munich': 'https://www.holiday-weather.com/munich/averages/',
    'Naples': 'https://www.holiday-weather.com/naples/averages/',
    'New York': 'https://www.holiday-weather.com/new_york/averages/',
    'Nice': 'https://www.holiday-weather.com/nice/averages/',
    'Pattaya': 'https://www.holiday-weather.com/pattaya/averages/',
    'Phuket': 'https://www.holiday-weather.com/phuket/averages/',
    'Porto': 'https://www.holiday-weather.com/porto/averages/',
    'Quebec City': 'https://www.holiday-weather.com/quebec/averages/',
    'San Francisco': 'https://www.holiday-weather.com/san_francisco/averages/',
    'Thimphu': 'https://www.holiday-weather.com/thimphu/averages/',
    'Valparaíso': 'https://www.holiday-weather.com/valparaiso/averages/',
    'Venice': 'https://www.holiday-weather.com/venice/averages/',
    'Victoria': 'https://www.holiday-weather.com/victoria/averages/',
    'Yogyakarta': 'https://www.holiday-weather.com/yogyakarta/averages/'
}


# Function to scrape temperature data for a city
def scrape_city_temperatures(city, url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        chart_div = soup.find("div", {"data-chart": True})
        if chart_div:
            chart_data = json.loads(chart_div["data-chart"])
            for series in chart_data["series"]:
                if series["name"] == "Centigrade":
                    return series["data"]
    print(f"Temperature data not found for {city}.")
    return None


# Loop through each city, scrape data, and insert into MySQL
for city, url in city_urls.items():
    print(f"Processing {city}...")
    temperatures = scrape_city_temperatures(city, url)
    if temperatures and len(temperatures) == 12:
        # Insert temperatures into the database
        try:
            insert_query = """
            INSERT INTO weather (city, january_avg_temp, february_avg_temp, march_avg_temp,
                                 april_avg_temp, may_avg_temp, june_avg_temp, july_avg_temp,
                                 august_avg_temp, september_avg_temp, october_avg_temp,
                                 november_avg_temp, december_avg_temp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                january_avg_temp = VALUES(january_avg_temp),
                february_avg_temp = VALUES(february_avg_temp),
                march_avg_temp = VALUES(march_avg_temp),
                april_avg_temp = VALUES(april_avg_temp),
                may_avg_temp = VALUES(may_avg_temp),
                june_avg_temp = VALUES(june_avg_temp),
                july_avg_temp = VALUES(july_avg_temp),
                august_avg_temp = VALUES(august_avg_temp),
                september_avg_temp = VALUES(september_avg_temp),
                october_avg_temp = VALUES(october_avg_temp),
                november_avg_temp = VALUES(november_avg_temp),
                december_avg_temp = VALUES(december_avg_temp)
            """
            cursor.execute(insert_query, [city] + temperatures)
            conn.commit()
            print(f"Inserted/Updated temperature data for {city}")
        except mysql.connector.Error as err:
            print(f"Error inserting data for {city}: {err}")
    else:
        print(f"Skipped {city} due to incomplete data.")

    # Sleep to avoid overloading the server with requests
    time.sleep(2)

# Close the cursor and connection
cursor.close()
conn.close()
