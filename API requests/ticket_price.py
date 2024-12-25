import requests

# Set up the parameters for the API request
url = "https://api.travelpayouts.com/v1/prices/cheap"
params = {
    "origin": "TLV",  # IATA code for Ben Gurion Airport
    "destination": "NYC",  # IATA code for New York City (all airports)
    "currency": "usd",  # Currency of prices
    "token": "d58a898b7e14deeb7b378a4df809aa70",  # Your API token
    "partner_id": "586989"  # Your Partner ID
}

# Make the request to the Aviasales API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Print the full response for debugging
    print("Full API Response:", data)

    if data.get("success"):
        flights = data.get("data", {}).get("NYC", {})
        if flights:
            print("Cheapest flights from TLV to NYC:")
            for flight_date, details in flights.items():
                print(f"Departure Date: {details['departure_at']}")
                print(f"Return Date: {details['return_at']}")
                print(f"Airline: {details['airline']}")
                print(f"Flight Number: {details['flight_number']}")
                print(f"Price: ${details['price']} USD")
                print(f"Expires At: {details['expires_at']}")

                # Check if 'link' exists in the response
                if 'link' in details:
                    print(f"Link: https://www.aviasales.com{details['link']}\n")
                else:
                    print("Link: Not available\n")
        else:
            print("No flight data found.")
    else:
        print("Request was not successful:", data)
else:
    print("Failed to retrieve data. Status code:", response.status_code)
