from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import subprocess
from typing import Tuple
import uuid
from const.general import INPUT_NAME, PATH, RESULTS_FOLDER, SCRAPER_NAME
from const.google_map_scraper import SCRAPER_DEPTH, SCRAPER_ZOOM
from server_connection import update_scraper_status

def update_status(func):
    def inner1(*args, **kwargs):
        update_scraper_status(ms_id=args[0], cell_id=args[1], status="scraping")
        print('scraping')
        func(*args, **kwargs)
        print('done')
        update_scraper_status(ms_id=args[0], cell_id=args[1], status="done")
    return inner1

@update_status
def run_scraper(ms_id: str, cell_id: str, cell_center: Tuple[float, float]):
    """
    Function to run the scraper command for a specific cell center.
    """
    scraper_command = f"{PATH}/{SCRAPER_NAME} -depth {SCRAPER_DEPTH} -zoom {SCRAPER_ZOOM} " \
    f"-geo {cell_center[0]},{cell_center[1]} " \
    f"-input {PATH}/{INPUT_NAME} " \
    f"-results {RESULTS_FOLDER}/{str(uuid.uuid4())}.csv " \
    f"-exit-on-inactivity 10m"

    # Run the scraper
    # os.system(scraper_command)
    process = subprocess.Popen(scraper_command, shell=True)

    process.wait()

def scan_cells(ms_id: str, cell_centers: dict[str, Tuple[float, float]]):
    """
    Run all scraper commands in parallel using threading.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_scraper, ms_id, cell_id, cell_center) for cell_id, cell_center in cell_centers.items()]

        for future in futures:
            results.append(future.result())
    return results
