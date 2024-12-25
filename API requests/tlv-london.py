import requests
from datetime import datetime, timedelta

# Define the API endpoint and base parameters
url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
base_params = {
    "origin": "TLV",
    "currency": "usd",
    "token": "d58a898b7e14deeb7b378a4df809aa70",  # Replace with your actual API token
    "partner_id": "586989",  # Replace with your actual partner ID
    "sorting": "price",
    "one_way": "false",  # To include round-trip flights
    "direct": "false",  # To include flights with transfers
    "limit": 100  # Set a high limit to capture as many flights as possible per request
}

# List of destination cities with their IATA codes
destinations = {
    "New York": "JFK",
    "London": "LHR",
    "Paris": "CDG",
    "Bangkok": "BKK",
    "Dubai": "DXB",
    "Vienna": "VIE",
    "Barcelona": "BCN",
    "Moscow": "SVO",
    "Lima": "LIM",
    "Rio de Janeiro": "GIG",
    "Dubrovnik": "DBV",
    "Naples": "NAP"
}

# Define the date range
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 8, 1)

# Dictionary to store the count of flights per month for each destination
flight_counts = {destination: {} for destination in destinations}

# Iterate through each destination
for city, iata_code in destinations.items():
    print(f"Fetching data for {city} ({iata_code})...\n")

    # Iterate through each month in the date range
    current_date = start_date
    while current_date <= end_date:
        # Format the date as YYYY-MM
        depart_date = current_date.strftime("%Y-%m")

        # Update the parameters with the current departure date and destination
        params = base_params.copy()
        params["destination"] = iata_code
        params["departure_at"] = depart_date

        # Send the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                flights = data.get("data", [])
                # Store the count of flights for the current month and destination
                flight_counts[city][depart_date] = len(flights)
                print(f"Number of flights for {city} in {depart_date}: {len(flights)}")
            else:
                print(f"Request was not successful for {city} in {depart_date}. Response: {data}")
                flight_counts[city][depart_date] = 0  # Record 0 if unsuccessful
        else:
            print(f"Failed to retrieve data for {city} in {depart_date}. Status code: {response.status_code}")
            flight_counts[city][depart_date] = 0  # Record 0 if request failed

        # Move to the next month
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)

    print("\n")

# Print the final summary of flight counts per month for each destination
print("\nSummary of Flight Counts Per Month for Each Destination:")
for city, counts in flight_counts.items():
    print(f"\n{city}:")
    for month, count in counts.items():
        print(f"  {month}: {count} flights")
