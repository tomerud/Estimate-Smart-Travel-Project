import mysql.connector

# Database connection information
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "112145"
DB_PORT = 3306
DB_NAME = "cities"

# Connect to the MySQL database
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    database=DB_NAME
)

cursor = connection.cursor()

# List of city price updates (city, budget_price, midrange_price, luxury_price)
price_updates = [
    ("Tel Aviv", 67, 159, 338),
    ("Las Vegas", 139, 369, 1037),
    ("New York", 131, 363, 1101),
    ("Pattaya", 44, 88, 179)
]

# Update statement to set prices for each city
update_query = """
    UPDATE top_touristic_cities
    SET budget_price_usd = %s,
        midrange_price_usd = %s,
        luxury_price_usd = %s
    WHERE city = %s
"""

# Execute the update for each city in the list
for city, budget_price, midrange_price, luxury_price in price_updates:
    cursor.execute(update_query, (budget_price, midrange_price, luxury_price, city))
    print(f"Prices for {city} updated successfully.")

# Commit the changes to save the updates
connection.commit()

# Close the connection
cursor.close()
connection.close()

print("All specified city prices updated successfully.")
