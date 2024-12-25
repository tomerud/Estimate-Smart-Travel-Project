import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def normalize_and_update(source_table, target_table, column_mappings):
    """
    Generalized function to normalize columns from a source table and update the target table.

    :param source_table: Name of the source table (e.g., 'top_touristic_cities', 'weather').
    :param target_table: Name of the target table (e.g., 'normalized_data').
    :param column_mappings: A list of tuples where each tuple contains:
                            (source_column, target_column)
                            - source_column: The column name in the source table.
                            - target_column: The column name to update in the target table.
    """
    # Retrieve database credentials from environment variables
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor(dictionary=True)

    try:
        for source_column, target_column in column_mappings: # for each pair of source column and target column
            print(f"Normalizing and updating column: {source_column} -> {target_column}")

            # Fetch the data for the column- rows will have pairs of city_id, source_collumn value
            query = f"SELECT city_id, {source_column} FROM {source_table};"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Extract values for normalization
            values = []
            for row in rows:
                if row[source_column] is not None:
                    values.append(row[source_column])

            # Calculate max and min values
            if not values:
                print(f"No data found for column: {source_column}")
                continue

            value_max = max(values)
            value_min = min(values)

            # Normalize values and prepare update data
            update_data = []
            for row in rows:
                value = row[source_column]
                normalized_value = (
                    (value - value_min) / (value_max - value_min)
                    if value is not None else None
                )
                update_data.append((normalized_value, row['city_id']))

            # Update the target table
            update_query = f"""
                UPDATE {target_table}
                SET {target_column} = %s
                WHERE city_id = %s;
            """
            cursor.executemany(update_query, update_data)
            connection.commit()

            print(f"Column {source_column} normalized and updated as {target_column}.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


normalize_and_update(
    source_table='weather',
    target_table='normalized_data',
    column_mappings=[
        ('january_avg_temp', 'january_avg_temp_norm'),
        ('february_avg_temp', 'february_avg_temp_norm'),
        ('march_avg_temp', 'march_avg_temp_norm'),
        ('april_avg_temp', 'april_avg_temp_norm'),
        ('may_avg_temp', 'may_avg_temp_norm'),
        ('june_avg_temp', 'june_avg_temp_norm'),
        ('july_avg_temp', 'july_avg_temp_norm'),
        ('august_avg_temp', 'august_avg_temp_norm'),
        ('september_avg_temp', 'september_avg_temp_norm'),
        ('october_avg_temp', 'october_avg_temp_norm'),
        ('november_avg_temp', 'november_avg_temp_norm'),
        ('december_avg_temp', 'december_avg_temp_norm')
    ]
)
