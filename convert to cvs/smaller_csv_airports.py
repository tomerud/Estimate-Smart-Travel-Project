import pandas as pd

# Load the CSV file from the provided path
file_path = r"C:\Estimate\convert to cvs\airports.csv"
airports_df = pd.read_csv(file_path)

# Filter for rows where 'type' is 'large_airport' and select only specified columns
large_airports_df = airports_df[airports_df['type'] == 'large_airport'][['iata_code', 'name', 'municipality', 'latitude_deg', 'longitude_deg']]

# Save the filtered data to a new CSV file
output_path = r"C:\Estimate\convert to cvs\large_airports.csv"
large_airports_df.to_csv(output_path, index=False)

print(f"Filtered CSV saved to: {output_path}")
