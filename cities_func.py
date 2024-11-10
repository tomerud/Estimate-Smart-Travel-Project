import mysql.connector

# Replace with your MySQL credentials
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="112145",
    port=3306,
    database="cities"
)
cursor = conn.cursor()

# Example query to fetch data from a table
cursor.execute("SELECT * FROM cities.cities;")
result = cursor.fetchall()

for row in result:
    print(row)

# Close the connection
cursor.close()
conn.close()