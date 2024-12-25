import requests
from datetime import datetime, timedelta

# Define the API endpoint and base parameters
url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
base_params = {
    "origin": "TLV",
    "destination": "JFK",
    "currency": "usd",
    "token": "d58a898b7e14deeb7b378a4df809aa70",  # Replace with your actual API token
    "partner_id": "586989",  # Replace with your actual partner ID
    "sorting": "price",
    "one_way": "false",  # To include round-trip flights
    "direct": "false",  # To include flights with transfers
    "limit": 100  # Set a high limit to capture as many flights as possible per request
}

# Define the date range
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 8, 1)

# Dictionary to store the count of flights per month
flight_counts = {}

# Iterate through each month in the date range
current_date = start_date
while current_date <= end_date:
    # Format the date as YYYY-MM
    depart_date = current_date.strftime("%Y-%m")

    # Update the parameters with the current departure date
    params = base_params.copy()
    params["departure_at"] = depart_date

    # Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            flights = data.get("data", [])
            # Store the count of flights for the current month
            flight_counts[depart_date] = len(flights)
            print(f"Number of flights for {depart_date}: {len(flights)}")
        else:
            print(f"Request was not successful for {depart_date}. Response: {data}")
            flight_counts[depart_date] = 0  # Record 0 if unsuccessful
    else:
        print(f"Failed to retrieve data for {depart_date}. Status code: {response.status_code}")
        flight_counts[depart_date] = 0  # Record 0 if request failed

    # Move to the next month
    current_date += timedelta(days=32)
    current_date = current_date.replace(day=1)

# Print the final summary of flight counts per month
print("\nSummary of Flight Counts Per Month:")
for month, count in flight_counts.items():
    print(f"{month}: {count} flights")
