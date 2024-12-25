import mysql.connector
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

# Query to show columns
cursor.execute("SHOW COLUMNS FROM tel_aviv_flights")
columns = cursor.fetchall()
print("Table Structure:")
for column in columns:
    print(column)

# Query to show indexes
cursor.execute("SHOW INDEXES FROM tel_aviv_flights")
indexes = cursor.fetchall()
print("\nIndexes and Keys:")
for index in indexes:
    print(index)

# Close the cursor and connection
cursor.close()
conn.close()
