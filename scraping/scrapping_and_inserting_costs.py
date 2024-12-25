import requests
from bs4 import BeautifulSoup
import mysql.connector
import json
import time

# Database connection information
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "112145"
DB_PORT = 3306
DB_NAME = "cities"

# List of cities with geonameid values
cities = {
"Las Vegas": 5506956 #and more
}


# Step 1: Function to scrape daily costs for each city
def get_daily_costs(geonameid):
    url_template = "https://www.budgetyourtrip.com/budgetreportadv.php?geonameid={}&countrysearch=&country_code=&categoryid=0&budgettype={}&triptype=0&startdate=&enddate=&travelerno=0"
    travel_styles = {'budget': 1, 'midrange': 2, 'luxury': 3}
    costs = {}

    for style, budgettype in travel_styles.items():
        city_url = url_template.format(geonameid, budgettype)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        response = requests.get(city_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        cost_element = soup.find("span", class_="curvalue")
        if cost_element:
            costs[style] = cost_element.get_text(strip=True)
        else:
            print(f"Unable to find cost value for {style} travel style.")

    return costs


# Scrape costs for all cities
all_city_costs = {}
for city_name, geonameid in cities.items():
    print(f"Fetching data for {city_name}...")
    all_city_costs[city_name] = get_daily_costs(geonameid)
    time.sleep(1)  # Delay to avoid overloading the server

# Step 2: Save scraped data to JSON
with open('city_costs.json', 'w') as f:
    json.dump(all_city_costs, f, indent=4)
print("city_costs.json has been created.")

# Step 3: Connect to MySQL and add columns if not present
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    database=DB_NAME
)
cursor = connection.cursor()

# Add columns for prices
for column in ['budget_price_usd', 'midrange_price_usd', 'luxury_price_usd']:
    try:
        cursor.execute(f"""
            ALTER TABLE top_touristic_cities
            ADD COLUMN {column} DECIMAL(10, 2)
        """)
        print(f"Column {column} added successfully.")
    except mysql.connector.Error as err:
        if "Duplicate column name" in str(err):
            print(f"Column {column} already exists.")
        else:
            print(f"Error adding column {column}: {err}")

# Step 4: Insert data into the table
for city, costs in all_city_costs.items():
    try:
        # Handle missing data
        budget_price = float(costs.get('budget', '0').replace('$', ''))
        midrange_price = float(costs.get('midrange', '0').replace('$', ''))
        luxury_price = float(costs.get('luxury', '0').replace('$', ''))

        update_query = """
            UPDATE top_touristic_cities
            SET budget_price_usd = %s,
                midrange_price_usd = %s,
                luxury_price_usd = %s
            WHERE city = %s
        """
        cursor.execute(update_query, (budget_price, midrange_price, luxury_price, city))
        print(f"Updated data for {city}.")

    except mysql.connector.Error as err:
        print(f"Error updating data for {city}: {err}")
    except ValueError:
        print(f"Data conversion error for {city}. Skipping this city.")

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Data has been successfully updated in the database.")
