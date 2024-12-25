import requests
from datetime import datetime

# Define the API endpoint and base parameters
url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
base_params = {
    "origin": "TLV",  # Set origin to Los Angeles (LAX)
    "destination": "JFK",  # Set destination to San Francisco (SFO)
    "currency": "usd",
    "token": "d58a898b7e14deeb7b378a4df809aa70",  # Replace with your actual API token
    "partner_id": "586989",  # Replace with your actual partner ID
    "sorting": "price",
    "one_way": "false",
    "direct": "false",
    "limit": 100
}

# Set December 2024 as the specific month to retrieve flights
params = base_params.copy()
params["departure_at"] = "2024-12"  # December 2024

# Send the GET request for December flights
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        flights = data.get("data", [])
        print(f"\nTotal flights found for December 2024 from Los Angeles to San Francisco: {len(flights)}")
        for idx, flight in enumerate(flights, start=1):
            # Print detailed information for each flight
            print(f"\nFlight {idx}:")
            print(f"Price: ${flight.get('price', 'N/A')}")
            print(f"Airline: {flight.get('airline', 'N/A')}")
            print(f"Departure Date: {flight.get('departure_at', 'N/A')}")
            print(f"Return Date: {flight.get('return_at', 'N/A')}")

            # Check if 'duration' is a dictionary before trying to access 'total'
            duration = flight.get('duration')
            if isinstance(duration, dict):
                print(f"Flight Duration: {duration.get('total', 'N/A')} minutes")
            else:
                print("Flight Duration: N/A")

            print(f"Transfers: {flight.get('transfers', 'N/A')}")
            print(f"Available Seats: {flight.get('available_seats', 'N/A')}")
    else:
        print(f"Request was not successful for December. Response: {data}")
else:
    print(f"Failed to retrieve data for December 2024 from Los Angeles to San Francisco. Status code: {response.status_code}")
