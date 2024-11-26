import os
from const.general import PATH
from scraper import scan_cells
from server_connection import get_cell_centers
from dotenv import load_dotenv

load_dotenv() 

def main():
    # Get cell centers to scan
    cell_centers = get_cell_centers()
    # print(cell_centers)
    # return

    # Scan
    scan_cells(cell_centers)

    # Extract results
    
    # Send results to server
    pass

if __name__ == "__main__":
    os.system(f'mkdir {PATH}/results')
    main()






