import subprocess
import time
from typing import Tuple
from const.general import INPUT_NAME, PATH, RESULTS_FOLDER, SCRAPER_NAME
from const.google_map_scraper import SCRAPER_DEPTH, SCRAPER_ZOOM
from server_connection import ScraperQuery, create_session, get_scraper_queries, mark_session_as_done, mark_session_as_scraping, save_locations

# def update_status(func):
#     def inner1(*args, **kwargs):
#         ms_id = kwargs['ms_id']
#         cell_id = kwargs['cell_id']
#         try:
#             update_scraper_status(ms_id=ms_id, cell_id=cell_id, status="scraping")
#             func(*args, **kwargs)
#             # Extract results and Send results to server
#             save_scraped_locations(cell_id=cell_id)
#             print('all saved')
#             update_scraper_status(ms_id=ms_id, cell_id=cell_id, status="done")
#             print('done')
#         except Exception as e:
#             update_scraper_status(ms_id=ms_id, cell_id=cell_id, status="error")
#             print(e)
#     return inner1

def run_scraper(cell_id: str, cell_center: Tuple[float, float]):
    session_id = create_session(cell_id=cell_id)
    print(f'WorldScraper -> Session Created: {session_id}')

    queries: list[ScraperQuery]
    try:
        print(f'WorldScraper -> Fetching Queries')
        queries = get_scraper_queries(id_cell=cell_id)
    except Exception as e:
        print(f'WorldScraper -> Error while fetching queries: {e}')
        mark_session_as_done(session_id=session_id, remarks=f"Error: Failed to fetch queries: {e}")
        return
    
    if not queries:
        print(f'WorldScraper -> No Queries Found - Marking session as done')
        mark_session_as_done(session_id=session_id,remarks="Error: No queries found")
        return
    
    print(f'WorldScraper -> Queries Fetched: {[q.value for q in queries]}')
    
    print(f'WorldScraper -> Setting up input queries in input.txt')
    process = subprocess.Popen(f'echo "{"\n".join([q.value for q in queries])}" | sudo tee {PATH}/{INPUT_NAME} > /dev/null', shell=True)
    process.wait()

    mark_session_as_scraping(session_id=session_id, queries=queries)
    
    scraper_command = f"sudo {PATH}/{SCRAPER_NAME} " \
    f"-geo {cell_center[0]},{cell_center[1]} " \
    f"-radius 550 " \
    f"-zoom {SCRAPER_ZOOM} " \
    f"-input {PATH}/{INPUT_NAME} " \
    f"-results {RESULTS_FOLDER}/{cell_id}.csv " \
    f"-exit-on-inactivity 3m " \
    f"-limit"
    print(f'WorldScraper -> Scraping session starting with command: {scraper_command}')

    # Run the scraper
    process = subprocess.Popen(scraper_command, shell=True)
    process.wait()
    print(scraper_command)
    time.sleep(5)


    try:
        print(f'WorldScraper -> Saving locations')
        save_locations(session_id=session_id, cell_id=cell_id)
    except Exception as e:
        print(f'WorldScraper -> Error while saving locations: {e}')
        mark_session_as_done(session_id=session_id, remarks=f"Error: Failed to save locations: {e}")
        return
    
    print(f'WorldScraper -> Scraper Done - Marking session as done')
    mark_session_as_done(session_id=session_id, remarks=f"Successfully scraped {cell_id}")

def scan_cells(cells: dict[str, tuple[float, float]]):
    """
    Run all scraper commands in parallel using threading.
    """
    [run_scraper(cell_id=cell_id, cell_center=cell_center) for cell_id, cell_center in cells.items()]
