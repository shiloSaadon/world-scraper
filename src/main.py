import os
from dotenv import load_dotenv
load_dotenv() 

from const.general import config
from scraper import scan_cells
from server_connection import get_scraper_hexagons
from dotenv import load_dotenv

def init():
    # Clear the results folder
    os.system(f'sudo rm -rf {config["PATH"]}/results')
    # Ensure that the results folder is there
    os.system(f'sudo mkdir {config["PATH"]}/results')

def main():
    # Get cell centers to scan
    # this will run until all hexagons have been scraped
    # or hit the limit
    print(f"Running world-scraper with configuration {config}")

    total_hexagons = 0
    while total_hexagons <= config["MAX_HEXAGON_COUNT"]:
        cells = get_scraper_hexagons()
        if not cells:
            return
        
        total_hexagons += len(cells)
        
        # Scan and save locations
        scan_cells(cells)
        print('cells done')

    print('crawl complete')
    pass


if __name__ == "__main__":
    init()
    main()
