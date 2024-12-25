import mysql.connector
import json

# Database connection information
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "112145"
DB_PORT = 3306
DB_NAME = "cities"

# Load city costs from the JSON file created in the previous step
with open('city_costs.json') as f:
    city_costs = json.load(f)

# Connect to the MySQL database
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    database=DB_NAME
)

cursor = connection.cursor()

# Step 1: Add the new columns if they don’t exist
try:
    cursor.execute("""
        ALTER TABLE cities
        ADD COLUMN IF NOT EXISTS budget_price_usd DECIMAL(10, 2),
        ADD COLUMN IF NOT EXISTS midrange_price_usd DECIMAL(10, 2),
        ADD COLUMN IF NOT EXISTS luxury_price_usd DECIMAL(10, 2)
    """)
    print("Columns added successfully (if they didn't already exist).")
except mysql.connector.Error as err:
    print(f"Error adding columns: {err}")

# Step 2: Insert the data into the table
for city, costs in city_costs.items():
    try:
        # Extract and clean the price data
        budget_price = float(costs['budget'].replace('$', ''))
        midrange_price = float(costs['midrange'].replace('$', ''))
        luxury_price = float(costs['luxury'].replace('$', ''))

        # Update statement
        update_query = """
            UPDATE cities
            SET budget_price_usd = %s,
                midrange_price_usd = %s,
                luxury_price_usd = %s
            WHERE city_name = %s
        """

        # Execute the update with values
        cursor.execute(update_query, (budget_price, midrange_price, luxury_price, city))
        print(f"Updated data for {city}.")

    except mysql.connector.Error as err:
        print(f"Error updating data for {city}: {err}")
    except ValueError:
        print(f"Data conversion error for {city}. Skipping this city.")

# Commit the changes to the database
connection.commit()

# Close the database connection
cursor.close()
connection.close()

print("Data has been successfully updated in the database.")
