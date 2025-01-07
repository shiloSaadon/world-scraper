import csv
import json
import os
from typing import Any
import uuid
from supabase import create_client
import h3
from const.general import QUERIES_COUNT, RESULTS_FOLDER
from const.h3 import H3_RES
from utils.utils import ScraperQuery

def create_session(cell_id: str) -> str:
    session_id = str(uuid.uuid4())
    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    spClient.schema('host_scraper').from_('sessions').insert({"id": session_id, "id_cell": cell_id}).execute()
    return session_id

def mark_session_as_scraping(session_id: str, queries: list[ScraperQuery]):
    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    spClient.schema('host_scraper').from_('sessions').update({"started_at": "now()"}).eq("id", session_id).execute()
    spClient.schema('host_scraper').from_('session_queries').insert([{"id_session": session_id, "id_query": q.id} for q in queries]).execute()

def mark_session_as_done(session_id: str, remarks: str):
    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    spClient.schema('host_scraper').from_('sessions').update({"completed_at": "now()", "remarks": remarks}).eq("id", session_id).execute()

def save_locations(session_id: str, cell_id: str):
    # Dict to hold all locations
    # using a dict ensures that we store unique locations
    all_locations: dict[str, dict[str, Any]] = {}
    
    # Get csv data
    data = list(csv.DictReader(open(f'{RESULTS_FOLDER}/{cell_id}.csv')))
    if not data:
        print(f'No data in {RESULTS_FOLDER}/{cell_id}.csv')
        return

    # Loop over all locations
    for row in data:
        row['id_cell'] = h3.latlng_to_cell(float(row['latitude']), float(row['longitude']), H3_RES)

        # Convert all nested objects to valid json
        row['menu'] = json.loads(row['menu'])

        #! Still need to handle cases when about is empty, null or not there
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
        all_locations[row['cid']] = row
    
    dataToBeUpserted = [loc_data for _, loc_data in all_locations.items()]

    if not dataToBeUpserted:
        return

    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    spClient.schema('host_scraper').rpc('ifn_scraper_locations_save', params={"p_id_session": session_id, "p_locations": dataToBeUpserted}).execute()

    
def get_scraper_hexagons() -> dict[str, tuple[float, float]] | None:
    try:
        spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
        
        hexRes = spClient.schema('host_scraper').rpc('ifn_scraper_cells_get', {"p_limit": os.environ['HEXAGON_COUNT']}).execute()
        if len(hexRes.data) == 0:
            raise Exception("No hexagons available")
        
        hexagons = { item['id']: h3.cell_to_latlng(item['id']) for item in hexRes.data }
        
        return {} if hexagons is None else {
            k: tuple(v) if isinstance(v, list) else v 
            for k, v in hexagons.items()
        }
    except Exception as e:
        print(f'Failed to fetch hexagons. Exception: {e}')
        return None

def get_scraper_queries(id_cell: str) -> list[ScraperQuery]:
    spClient = create_client(os.environ['SUPABASE_PROJECT_URL'] , os.environ['SUPABASE_PROJECT_KEY'])
    
    res = spClient.schema('host_scraper').rpc('ifn_scraper_queries_get', {"p_id_cell": id_cell, "p_limit": QUERIES_COUNT}).execute()
    
    return [ScraperQuery(id=item['id'], value=item['value']) for item in res.data]