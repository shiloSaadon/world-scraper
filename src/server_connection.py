import csv
import json
import os
from typing import Tuple
import requests
from supabase import create_client
from const.general import RESULTS_FOLDER
from const.h3 import AMOUNT_OF_HEXAGONS
from const.server_data import ENDPOINT

def get_cell_centers(ms_id: str) -> dict[str, Tuple[float, float]]:
    try:
        # Define the request headers
        HEADERS = {
            "Authorization": f"Bearer {os.environ['HOST_SERVER_AUTH_KEY']}",
            "Content-Type": "application/json"
        }

        # Define the query parameters
        PARAMS = {
            "ms_id": ms_id,
            "amount_of_hexagons": AMOUNT_OF_HEXAGONS
        }

        # Send he GET request
        response = requests.get(f"{os.environ['HOST_SERVER_URL']}{ENDPOINT}", headers=HEADERS, params=PARAMS)

        # Handle the response
        if response.status_code == 200:
            # Successfully retrieved hexagons
            return { id: (cell_center[0], cell_center[1]) for id, cell_center in response.json().get("hexagons").items() }
        else:
            # Print the error details
            print(f"Failed to fetch hexagons. Status code: {response.status_code}")
            print("Response:", response.json())
            return {}
    
    except Exception as e:
        print(f'Failed to fetch hexagons. Exception: {e}')
        return {}
    
def save_scraped_locations(cell_id: str):
    # Dict to hold all locations
    # using a dict ensures that we store unique locations
    all_locations = {}
    
    # Get csv data
    data = list(csv.DictReader(open(f'{RESULTS_FOLDER}/{cell_id}.csv')))
    if not data:
        raise Exception(f'No data in {RESULTS_FOLDER}/{cell_id}.csv')

    # Loop over all locations
    for row in data:
        # Set id for compatibility with frontend
        row['id'] = row['cid']
        
        # remove cid
        del row['cid']
        
        # remove input_id as it is not required
        del row['input_id']

        # Convert all nested objects to valid json
        row['menu'] = json.loads(row['menu'])
        row['about'] = json.loads(row['about'])
        row['owner'] = json.loads(row['owner'])
        row['images'] = json.loads(row['images'])
        row['open_hours'] = json.loads(row['open_hours'])
        row['order_online'] = json.loads(row['order_online'])
        row['user_reviews'] = json.loads(row['user_reviews'])
        row['popular_times'] = json.loads(row['popular_times'])
        row['complete_address'] = json.loads(row['complete_address'])
        row['reviews_per_rating'] = json.loads(row['reviews_per_rating'])
        
        # Add data to all_locations
        all_locations[row['id']] = row
    
    dataToBeUpserted = [{"type": "scraped_gmaps", "id_external": loc_id, "metadata": loc_data} for loc_id, loc_data in all_locations.items()]

    if not dataToBeUpserted:
        return

    [print(d['metadata']['title']) for d in dataToBeUpserted]

    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    # Upsert parsed locations with a conflict on id_external so same locations can be ignored
    spClient.from_('locations').upsert(
        dataToBeUpserted, 
        on_conflict="id_external"
    ).execute()


def update_scraper_status(ms_id: str, cell_id: str, status: str):
    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    spClient.schema('host_scraper').from_('logs').insert({"id_ms": ms_id, "id_cell": cell_id, "status": status}).execute()

# initiated
# scraping
# done - error