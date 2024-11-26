import os
import requests
import uuid
from const.server_data import BASE_URL, ENDPOINT


def get_cell_centers():
    try:
        # Define the request headers
        HEADERS = {
            "Authorization": f"Bearer {os.environ['HOST_SERVER_AUTH_KEY']}",
            "Content-Type": "application/json"
        }

        # Define the query parameters
        PARAMS = {
            "ms_id": str(uuid.uuid4()),
            "amount_of_hexagons": 15
        }

        # Send the GET request
        response = requests.get(f"{BASE_URL}{ENDPOINT}", headers=HEADERS, params=PARAMS)

        # Handle the response
        if response.status_code == 200:
            # Successfully retrieved hexagons
            return response.json().get("hexagons")
        else:
            # Print the error details
            print(f"Failed to fetch hexagons. Status code: {response.status_code}")
            print("Response:", response.json())
            return []
    
    except Exception as e:
        return []