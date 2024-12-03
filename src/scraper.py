from concurrent.futures import ThreadPoolExecutor
import subprocess
from typing import Tuple
from const.general import INPUT_NAME, PATH, RESULTS_FOLDER, SCRAPER_NAME
from const.google_map_scraper import SCRAPER_DEPTH, SCRAPER_ZOOM
from server_connection import save_scraped_locations, update_scraper_status

def update_status(func):
    def inner1(*args, **kwargs):
        ms_id = kwargs['ms_id']
        cell_id = kwargs['cell_id']
        try:
            update_scraper_status(ms_id=ms_id, cell_id=cell_id, status="scraping")
            print('scraping')
            func(*args, **kwargs)
            # Extract results and Send results to server
            save_scraped_locations(cell_id=cell_id)
            print('all saved')
            update_scraper_status(ms_id=ms_id, cell_id=cell_id, status="done")
            print('done')
        except Exception as e:
            update_scraper_status(ms_id=ms_id, cell_id=cell_id, status="error")
            print(e)
    return inner1

@update_status
def run_scraper(ms_id: str, cell_id: str, cell_center: Tuple[float, float]):
    """
    Function to run the scraper command for a specific cell center.
    """
    scraper_command = f"sudo {PATH}/{SCRAPER_NAME} -depth {SCRAPER_DEPTH} -zoom {SCRAPER_ZOOM} " \
    f"-c 1 " \
    f"-geo {cell_center[0]},{cell_center[1]} " \
    f"-input {PATH}/{INPUT_NAME} " \
    f"-results {RESULTS_FOLDER}/{cell_id}.csv " \
    f"-exit-on-inactivity 10m"

    # Run the scraper
    process = subprocess.Popen(scraper_command, shell=True)

    process.wait()

def scan_cells(ms_id: str, cell_centers: dict[str, Tuple[float, float]]):
    """
    Run all scraper commands in parallel using threading.
    """
    [run_scraper(ms_id=ms_id, cell_id=cell_id, cell_center=cell_center) for cell_id, cell_center in cell_centers.items()]
