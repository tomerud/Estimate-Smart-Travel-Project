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

# Delete query to remove rows with NULL or 0 in budget_price_usd
delete_query = """
    DELETE FROM top_touristic_cities
    WHERE budget_price_usd IS NULL OR budget_price_usd = 0
"""

# Execute the delete query
cursor.execute(delete_query)
connection.commit()

# Print number of rows deleted
print(f"Rows with NULL or 0 in budget_price_usd have been deleted successfully. Total rows affected: {cursor.rowcount}")

# Close the connection
cursor.close()
connection.close()
