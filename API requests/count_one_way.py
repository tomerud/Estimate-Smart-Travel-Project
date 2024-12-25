import requests

# Define the API endpoint and base parameters
url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
base_params = {
    "origin": "TLV",  # Tel Aviv Airport code
    "destination": "JFK",  # New York Airport code
    "currency": "usd",
    "token": "d58a898b7e14deeb7b378a4df809aa70",  # Replace with your actual API token
    "partner_id": "586989",  # Replace with your actual partner ID
    "sorting": "price",
    "one_way": "true",
    "direct": "false",
    "limit": 100
}

# Set the departure date to a specific month
params = base_params.copy()
params["departure_at"] = "2024-12"  # December 2024

# Send the GET request for flights
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        flights = data.get("data", [])
        print(f"\nTotal flights found for December 2024 from Tel Aviv to New York: {len(flights)}")
        for idx, flight in enumerate(flights, start=1):
            # Display the required details for each flight
            print(f"\nFlight {idx}:")
            print(f"Origin City (IATA): {flight.get('origin', 'N/A')}")
            print(f"Destination City (IATA): {flight.get('destination', 'N/A')}")
            print(f"Origin Airport: {flight.get('origin_airport', 'N/A')}")
            print(f"Destination Airport: {flight.get('destination_airport', 'N/A')}")
            print(f"Price: ${flight.get('price', 'N/A')} USD")
            print(f"Airline (IATA): {flight.get('airline', 'N/A')}")
            print(f"Flight Number: {flight.get('flight_number', 'N/A')}")
            print(f"Departure Date and Time: {flight.get('departure_at', 'N/A')}")
            print(f"Number of Transfers: {flight.get('transfers', 'N/A')}")
            print(f"Duration (to destination) in minutes: {flight.get('duration_to', 'N/A')}")

            # Optional: Print the link to book or view the flight
            print(f"Link: https://www.aviasales.com{flight.get('link', '')}")
    else:
        print(f"Request was not successful for December. Response: {data}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
