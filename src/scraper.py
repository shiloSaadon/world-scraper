import subprocess
import time
import os
from typing import Tuple
from const.general import INPUT_NAME, PATH, RESULTS_FOLDER, SCRAPER_NAME, QUERIES_BATCH_COUNT
from const.google_map_scraper import SCRAPER_ZOOM
from server_connection import ScraperQuery, create_session, get_scraper_queries, mark_session_as_done, mark_session_as_scraping, save_locations
from utils.utils import get_os

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

def run_scraper(cell_id: str, cell_center: Tuple[float, float], session_id: str):
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

    mark_session_as_scraping(session_id=session_id, queries=queries)

    # for i in range(0, len(queries), QUERIES_BATCH_COUNT):
        # batch = queries[i:i + QUERIES_BATCH_COUNT]
    batch_value = [q.value for q in queries]

    # print(f'WorldScraper -> Scraping batch [{queries}]')
    print(f'WorldScraper -> Setting up input queries in input.txt')
    process = subprocess.Popen(f'echo "{"\n".join(batch_value)}" | sudo tee {PATH}/{INPUT_NAME} > /dev/null', shell=True)
    process.wait()

    scraper_command = f"sudo {PATH}/go-scraper/{SCRAPER_NAME}_{get_os()} " \
    f"-geo {cell_center[0]},{cell_center[1]} " \
    f"-radius 550 " \
    f"-zoom {SCRAPER_ZOOM} " \
    f"-input {PATH}/{INPUT_NAME} " \
    f"-results {RESULTS_FOLDER}/{cell_id}.csv " \
    f"-exit-on-inactivity 1m " \
    f"-limit " \
    f"-resty-mode " \
    f"-check-mode"
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

    # cell_sessions store the cell information + the session id
    cell_sessions: dict[str, tuple[tuple[float, float], str]] = {
        cell_id: (center, create_session(cell_id=cell_id)) for cell_id, center in cells.items()
    }

    # run the
    [run_scraper(cell_id=cell_id, cell_center=cell_info[0], session_id=cell_info[1]) for cell_id, cell_info in cell_sessions.items()]
