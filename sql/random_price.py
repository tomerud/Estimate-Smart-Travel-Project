import mysql.connector
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to the MySQL database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Fetch cities and their continents from `top_touristic_cities`
cursor.execute("SELECT city, continent FROM top_touristic_cities")
city_data = cursor.fetchall()


# Define monthly price generation based on criteria
def get_monthly_prices(city, continent):
    prices = {}

    if continent == "Oceania":
        prices.update({month: int(random.gauss(1300, 100)) for month in range(3, 12)})
        prices.update({month: int(random.gauss(1400, 80)) for month in [12, 1, 2]})

    elif city in ["Athens", "Istanbul", "Berlin", "Rome"]:
        prices.update({month: int(random.gauss(280, 30)) for month in [9, 10, 11, 12, 1, 2, 3, 4, 5]})
        prices.update({month: int(random.gauss(320, 30)) for month in [6, 7, 8]})

    elif continent == "Europe":
        prices.update({month: int(random.gauss(350, 30)) for month in [9, 10, 11, 12, 1, 2, 3, 4, 5]})
        prices.update({month: int(random.gauss(400, 30)) for month in [6, 7, 8]})

    elif continent == "Middle East" and city == "Dubai":
        prices.update({month: int(random.gauss(280, 30)) for month in range(1, 13)})

    elif continent == "Asia":
        prices.update({month: int(random.gauss(500, 60)) for month in range(1, 13)})

    elif continent == "Africa":
        prices.update({month: int(random.gauss(440, 50)) for month in range(1, 13)})

    elif continent in ["South America", "Central America", "North America"]:
        prices.update({month: int(random.gauss(700, 80)) for month in range(1, 13)})
        for month in [12, 7, 8]:
            prices[month] = int(random.gauss(850, 80))

    else:
        # Default to "Rest of the World" category
        prices.update({month: int(random.gauss(800, 100)) for month in range(1, 13)})

    return prices


# Update `Tel_aviv_flights` table with generated monthly prices
for city, continent in city_data:
    monthly_prices = get_monthly_prices(city, continent)
    if monthly_prices:
        update_query = """
        UPDATE Tel_aviv_flights
        SET january_avg_price = %s, february_avg_price = %s, march_avg_price = %s,
            april_avg_price = %s, may_avg_price = %s, june_avg_price = %s,
            july_avg_price = %s, august_avg_price = %s, september_avg_price = %s,
            october_avg_price = %s, november_avg_price = %s, december_avg_price = %s
        WHERE destination = %s
        """
        cursor.execute(update_query, (
            monthly_prices.get(1), monthly_prices.get(2), monthly_prices.get(3),
            monthly_prices.get(4), monthly_prices.get(5), monthly_prices.get(6),
            monthly_prices.get(7), monthly_prices.get(8), monthly_prices.get(9),
            monthly_prices.get(10), monthly_prices.get(11), monthly_prices.get(12),
            city
        ))
        conn.commit()

print("Monthly prices updated in `Tel_aviv_flights` table.")

# Close the cursor and connection
cursor.close()
conn.close()
