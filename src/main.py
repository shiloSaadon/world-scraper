import os
import uuid
from const.general import PATH
from scraper import scan_cells
from server_connection import get_cell_centers
from dotenv import load_dotenv

def init():
    load_dotenv() 
    # Clear the results folder
    os.system(f'sudo rm -rf {PATH}/results')
    # Ensure that the results folder is there
    os.system(f'sudo mkdir {PATH}/results')

def main():
    ms_id = str(uuid.uuid4())
    # Get cell centers to scan
    cell_centers = get_cell_centers(ms_id)
    print(cell_centers)
    
    # Scan and save locations
    scan_cells(ms_id, cell_centers)
    print('all done')

    pass


if __name__ == "__main__":
    init()
    main()
