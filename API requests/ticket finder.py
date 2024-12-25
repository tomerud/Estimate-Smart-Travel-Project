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
    "one_way": "true",
    "limit": 100  # Adjust if you want more results per month
}

# Define the date range
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 8, 1)

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
            if flights:
                print(f"Flight data for {depart_date}:")
                for flight in flights:
                    print(f"  Price: ${flight['price']} USD")
                    print(f"  Airline: {flight['airline']}")
                    print(f"  Flight Number: {flight['flight_number']}")
                    print(f"  Departure Date: {flight['departure_at']}")
                    if 'link' in flight:
                        print(f"  Link: https://www.aviasales.com{flight['link']}\n")
                    else:
                        print("  Link: Not available\n")
            else:
                print(f"No flight data found for {depart_date}.")
        else:
            print(f"Request was not successful for {depart_date}. Response: {data}")
    else:
        print(f"Failed to retrieve data for {depart_date}. Status code: {response.status_code}")

    # Move to the next month
    current_date += timedelta(days=32)
    current_date = current_date.replace(day=1)
