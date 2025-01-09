import os
from const.general import PATH
from scraper import scan_cells
from server_connection import get_scraper_hexagons
from dotenv import load_dotenv

def init():
    load_dotenv() 
    # Clear the results folder
    os.system(f'sudo rm -rf {PATH}/results')
    # Ensure that the results folder is there
    os.system(f'sudo mkdir {PATH}/results')

def main():
    # Get cell centers to scan
    cells = get_scraper_hexagons()
    if not cells:
        return
    
    # Scan and save locations
    scan_cells(cells)
    print('all done')

    pass


if __name__ == "__main__":
    init()
    main()
