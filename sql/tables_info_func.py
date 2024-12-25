from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables from .env file
load_dotenv()

def inspect_tables(table_names):
    """
    Inspect the structure of specific tables in the database.
    :param table_names: List of table names to inspect.
    """
    # Connect to MySQL using environment variables
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 3306)),  # Default to 3306 if not set
        database=os.getenv("DB_NAME")
    )

    try:
        # Create a cursor
        cursor = conn.cursor()

        for table_name in table_names:
            print(f"Details for table '{table_name}':")

            # Query for columns
            print("\nColumns:")
            cursor.execute(f"SHOW COLUMNS FROM {table_name};")
            columns = cursor.fetchall()
            for column in columns:
                print(f"- {column[0]} (Type: {column[1]}, Null: {column[2]}, Key: {column[3]}, Default: {column[4]})")

            # Query for primary keys
            print("\nPrimary Key:")
            cursor.execute(f"""
                SELECT COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = '{os.getenv("DB_NAME")}' AND TABLE_NAME = '{table_name}' AND CONSTRAINT_NAME = 'PRIMARY';
            """)
            primary_keys = cursor.fetchall()
            if primary_keys:
                for pk in primary_keys:
                    print(f"- {pk[0]}")
            else:
                print("- None")

            # Query for foreign keys
            print("\nForeign Keys:")
            cursor.execute(f"""
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = '{os.getenv("DB_NAME")}' AND TABLE_NAME = '{table_name}' AND REFERENCED_TABLE_NAME IS NOT NULL;
            """)
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                for fk in foreign_keys:
                    print(f"- {fk[0]} -> {fk[1]}({fk[2]})")
            else:
                print("- None")

            # Query for indexes
            print("\nIndexes:")
            cursor.execute(f"SHOW INDEX FROM {table_name};")
            indexes = cursor.fetchall()
            for index in indexes:
                print(f"- Index Name: {index[2]}, Column: {index[4]}, Unique: {'Yes' if index[1] == 0 else 'No'}")

            print("\n" + "=" * 50 + "\n")  # Separator between tables

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


# Example usage
if __name__ == "__main__":
    # Replace with the table names you want to inspect
    tables_to_inspect = ['top_touristic_cities', 'language_mapping', 'languages', 'normalized_data']
    inspect_tables(tables_to_inspect)
