import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

# Create a cursor object
cursor = conn.cursor()

# Query to describe the table structure
describe_table_query = "DESCRIBE top_touristic_cities;"
cursor.execute(describe_table_query)
table_description = cursor.fetchall()
print("Table Structure:")
for column in table_description:
    print(column)

# Query to show indexes and keys
show_indexes_query = "SHOW INDEX FROM top_touristic_cities;"
cursor.execute(show_indexes_query)
indexes = cursor.fetchall()
print("\nIndexes and Keys:")
for index in indexes:
    print(index)

# Query to get full create table statement
show_create_table_query = "SHOW CREATE TABLE top_touristic_cities;"
cursor.execute(show_create_table_query)
create_table = cursor.fetchone()
print("\nCreate Table Statement:")
print(create_table[1])

# Close the cursor and connection
cursor.close()
conn.close()
