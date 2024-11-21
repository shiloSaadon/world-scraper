from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import uuid
from const.general import INPUT_NAME, PATH, RESULTS_FOLDER, SCRAPER_NAME
from const.google_map_scraper import SCRAPER_DEPTH, SCRAPER_ZOOM


def run_scraper(cell_center):
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
    

def scan_cells(cell_centers):
    """
    Run all scraper commands in parallel using threading.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_scraper, cell_center) for cell_center in cell_centers]
        for future in futures:
            results.append(future.result())
    return results
