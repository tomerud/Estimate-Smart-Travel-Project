import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
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

# Load the dataset using pandas
df = pd.read_csv('../Data/datasets/Average Temperature of Cities.csv')

# Clean the temperature data: extract only the Celsius part
for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
    df[month] = df[month].apply(lambda x: float(x.split('\n')[0].replace('"', '').strip()))

# Iterate over each row in the DataFrame (all cities)
for index, row in df.iterrows():
    city = row['City']
    # Query the top_touristic_cities table to check if the city exists
    cursor.execute("SELECT city FROM top_touristic_cities WHERE city = %s", (city,))
    result = cursor.fetchone()

    if result:
        # City exists in `top_touristic_cities`, prepare the temperature data
        temperatures = (
            city,
            row['Jan'], row['Feb'], row['Mar'], row['Apr'], row['May'],
            row['Jun'], row['Jul'], row['Aug'], row['Sep'], row['Oct'],
            row['Nov'], row['Dec']
        )

        # Insert temperatures into the weather table, or update if city already exists
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
        cursor.execute(insert_query, temperatures)
        conn.commit()
        print(f"Inserted or updated temperature data for {city}")
    else:
        print(f"City '{city}' not found in top_touristic_cities table, skipping.")

# Close the cursor and connection
cursor.close()
conn.close()
