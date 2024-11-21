import os
import h3

from const.general import INPUT_NAME, PATH, SCRAPER_NAME
from const.google_map_scraper import SCRAPER_DEPTH, SCRAPER_ZOOM
from const.h3 import H3_RES




# Generate the csv file name for the results
def RESULTS_NAME(cell: any): return f"results_{cell}.csv"

#  Scraper vars




# The plygone on the map that represent the area we want to scrape / get h3 data from
poly = h3.LatLngPoly([
    (32.0991252,34.7694704),
    (32.0932719,34.7671101),
    (32.0725096,34.7609303),
    (32.0671273,34.7713587),
    (32.0695275,34.7959063),
    (32.0846184,34.8002836),
    (32.0969075,34.7925160),
    (32.0991252,34.7694704),
])

# Ensure that the results folder is there
os.system(f'mkdir {PATH}/results')


# Get h3 hexagons called cells inside given polygone at `H3_RES + z` zoom
cells = h3.h3shape_to_cells(poly, H3_RES)
print(f'{len(cells)} cells at zoom {H3_RES}')

# Create the correct folder at the right zoom level
result_folder = f'{PATH}/results/zoom_{H3_RES}'
os.system('mkdir ' + result_folder)

## Loop over the first 10 cells
for c in range(min(len(cells), 1)):
    fine_name = f'zoom_{H3_RES}'
    cell = cells[c]

    # Get the center point of the current cell
    cell_center = h3.cell_to_latlng(cell)
    print(cell_center)
    
    # Define our scraper code on the center of the cell with the vars we defined to get places matching the queries in the `input.txt` file. also get path to save the results in
    scraper_command = f"{PATH}/{SCRAPER_NAME} -depth {SCRAPER_DEPTH} -zoom {SCRAPER_ZOOM} -geo {cell_center[0]},{cell_center[1]} -input {PATH}/{INPUT_NAME} -results {result_folder}/{RESULTS_NAME(cell)} -exit-on-inactivity 10m --debug"
    
    print(scraper_command)
    
    # Run the scraper
    os.system(scraper_command)


# 32.062911,34.776827,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 31.765663,35.204269,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 31.772946,35.214845,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 31.780095,35.221560,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 32.067031,34.781823,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.071541,34.769360,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 32.062911,34.776827,green,circle,"Results"
# 31.765663,35.204269,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.083319,34.781564,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 32.057344,34.770317,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 32.071541,34.769360,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 32.070409,34.773556,green,circle,"Results"
# 31.764757,35.220954,green,circle,"Results"
# 32.070409,34.773556,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.051662,34.778994,green,circle,"Results"
# 31.779404,35.221577,green,circle,"Results"
# 32.062911,34.776827,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.078823,34.779052,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 31.772946,35.214845,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 32.057344,34.770317,green,circle,"Results"
# 32.062372,34.775250,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 32.065048,34.787409,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 31.765663,35.204269,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 32.062911,34.776827,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 32.067031,34.781823,green,circle,"Results"
# 31.780095,35.221560,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 32.071541,34.769360,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 31.772946,35.214845,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.062911,34.776827,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 32.083319,34.781564,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 31.780095,35.221560,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 31.765663,35.204269,green,circle,"Results"
# 32.070409,34.773556,green,circle,"Results"
# 31.772946,35.214845,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"

# 31.765663,35.204269,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 32.083319,34.781564,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 32.057344,34.770317,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 32.062911,34.776827,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 32.070409,34.773556,green,circle,"Results"
# 32.071541,34.769360,green,circle,"Results"




# 32.062911,34.776827,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 31.780095,35.221560,green,circle,"Results"
# 32.070409,34.773556,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.057344,34.770317,green,circle,"Results"
# 32.083319,34.781564,green,circle,"Results"
# 31.772946,35.214845,green,circle,"Results"
# 32.077467,34.776731,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 32.071541,34.769360,green,circle,"Results"
# 32.086200,34.774599,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 32.064953,34.766610,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 31.765663,35.204269,green,circle,"Results"
# 32.052641,34.756142,green,circle,"Results"
# 32.067031,34.781823,green,circle,"Results"
# 32.071906,34.786175,green,circle,"Results"
# 32.082893,34.791633,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 32.071986,34.773739,green,circle,"Results"
# 31.779469,35.221069,green,circle,"Results"
# 32.078368,34.774441,green,circle,"Results"










# latitude	longitude
# 32.052641,34.756142,green,circle,"Results"
# 32.068361,34.768567,green,circle,"Results"
# 32.071986,34.773739,green,circle,"Results"
# 31.779404,35.221577,green,circle,"Results"
# 31.791068,34.638002,green,circle,"Results"
# 32.078823,34.779052,green,circle,"Results"
# 31.780095,35.221560,green,circle,"Results"
# 32.082893,34.791633,green,circle,"Results"
# 32.096631,34.772637,green,circle,"Results"
# 32.057344,34.770317,green,circle,"Results"
# 32.067031,34.781823,green,circle,"Results"
# 31.784995,35.211736,green,circle,"Results"
# 31.915075,35.016004,green,circle,"Results"
# 31.788021,35.229627,green,circle,"Results"
# 32.165629,34.821481,green,circle,"Results"
# 32.062372,34.775250,green,circle,"Results"
# 32.072837,34.771425,green,circle,"Results"
# 31.767424,35.187397,green,circle,"Results"
# 31.779956,35.187640,green,circle,"Results"
# 32.059697,34.772545,green,circle,"Results"
# 32.090680,34.782672,green,circle,"Results"
# 32.057265,34.771332,green,circle,"Results"
# 32.189241,34.810149,green,circle,"Results"
# 32.180191,34.875194,green,circle,"Results"
# 32.167892,34.840244,green,circle,"Results"
# 32.084729,34.774494,green,circle,"Results"
# 32.072499,34.788031,green,circle,"Results"
# 32.067372,34.774577,green,circle,"Results"
# 32.077165,34.774262,green,circle,"Results"
# 31.779469,35.221069,green,circle,"Results"
# 32.051662,34.778994,green,circle,"Results"
# 31.764757,35.220954,green,circle,"Results"
# 32.059867,34.771899,green,circle,"Results"
# 31.512313,34.427813,green,circle,"Results"
# 32.071906,34.786175,green,circle,"Results"
# 31.772946,35.214845,green,circle,"Results"
# 32.058186,34.766013,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 32.080069,34.822249,green,circle,"Results"
# 32.052274,34.755594,green,circle,"Results"
# 32.076841,34.815629,green,circle,"Results"
# 32.057686,34.811817,green,circle,"Results"
# 32.049445,34.757403,green,circle,"Results"
# 32.077809,34.814830,green,circle,"Results"
# 32.832304,34.977924,green,circle,"Results"
# 32.041966,34.751378,green,circle,"Results"
# 32.087641,34.774982,green,circle,"Results"
# 32.809854,34.993083,green,circle,"Results"
# 32.083793,34.776209,green,circle,"Results"
# 32.072056,34.778615,green,circle,"Results"
# 32.079870,34.774362,green,circle,"Results"
# 32.113320,34.824511,green,circle,"Results"
# 32.079542,34.777118,green,circle,"Results"
# 32.080919,34.770255,green,circle,"Results"
# 32.062911,34.776827,green,circle,"Results"
# 32.068989,34.768695,green,circle,"Results"
# 32.085724,34.774745,green,circle,"Results"
# 32.071182,34.769558,green,circle,"Results"
# 32.071541,34.769360,green,circle,"Results"
# 31.681284,34.557442,green,circle,"Results"
# 32.161081,34.795322,green,circle,"Results"
# 31.673513,34.568328,green,circle,"Results"
# 32.074510,34.770480,green,circle,"Results"
# 32.086200,34.774599,green,circle,"Results"
# 32.070409,34.773556,green,circle,"Results"
# 32.055195,34.751776,green,circle,"Results"
# 31.797441,34.633688,green,circle,"Results"
# 32.052224,34.763295,green,circle,"Results"
# 32.077467,34.776731,green,circle,"Results"
# 31.748575,35.206066,green,circle,"Results"
# 31.537063,35.098720,green,circle,"Results"
# 32.059921,34.771615,green,circle,"Results"
# 32.052547,34.752162,green,circle,"Results"
# 31.765663,35.204269,green,circle,"Results"
# 32.056278,34.770852,green,circle,"Results"
# 31.900090,34.808513,green,circle,"Results"









# from concurrent.futures import ThreadPoolExecutor, as_completed
# import os
# import subprocess
# import h3
# import requests
# import uuid

# from const.general import INPUT_NAME, MAX_THREADS, PATH, RESULTS_FOLDER, SCRAPER_NAME
# from const.google_map_scraper import INACTIVITY_TIMEOUT, SCRAPER_DEPTH, SCRAPER_ZOOM
# from const.h3 import H3_RES
# from const.server_data import BASE_URL, ENDPOINT



# def get_cell_centers():
#     # The plygone on the map that represent the area we want to scrape / get h3 data from
#     poly = h3.LatLngPoly([
#         (32.0991252,34.7694704),
#         (32.0932719,34.7671101),
#         (32.0725096,34.7609303),
#         (32.0671273,34.7713587),
#         (32.0695275,34.7959063),
#         (32.0846184,34.8002836),
#         (32.0969075,34.7925160),
#         (32.0991252,34.7694704),
#     ])
#     # Get h3 hexagons called cells inside given polygone at `H3_RES + z` zoom
#     cells = h3.h3shape_to_cells(poly, H3_RES)

#     return [h3.cell_to_latlng(cell) for cell in cells][:5]
#     try:
        
#         # Define the request headers
#         HEADERS = {
#             "Authorization": "Bearer your_jwt_token",  # Replace `your_jwt_token` with an actual JWT token
#             "Content-Type": "application/json"
#         }

#         # Define the query parameters
#         PARAMS = {
#             "ms_id": str(uuid.uuid4()),
#             "amount_of_hexagons": 15
#         }

#         # Send the GET request
#         response = requests.get(f"{BASE_URL}{ENDPOINT}", headers=HEADERS, params=PARAMS)

#         # Handle the response
#         if response.status_code == 200:
#             # Successfully retrieved hexagons
#             return response.json().get("hexagons")
#         else:
#             # Print the error details
#             print(f"Failed to fetch hexagons. Status code: {response.status_code}")
#             print("Response:", response.json())
#             return []
    
#     except Exception as e:
#         return []
    
# def run_scraper(cell_center):
#     """
#     Function to run the scraper command for a specific cell center.
#     """
#     # Generate a unique file name for the result
#     result_file = f"{RESULTS_FOLDER}/{uuid.uuid4()}.csv"

#     # Format the command
#     scraper_command = [
#         f"{PATH}/{SCRAPER_NAME}",
#         "-depth", str(SCRAPER_DEPTH),
#         "-zoom", str(SCRAPER_ZOOM),
#         "-geo", f"{cell_center[0]},{cell_center[1]}",
#         "-input", f"{PATH}/{INPUT_NAME}",
#         "-results", result_file,
#         "-exit-on-inactivity", INACTIVITY_TIMEOUT
#     ]

#     try:
#         # Run the scraper and wait for completion
#         result = subprocess.run(scraper_command, check=True, text=True, capture_output=True)

#         # Log success
#         return f"Success: {cell_center} -> Results saved to {result_file}"

#     except subprocess.CalledProcessError as e:
#         # Log errors
#         return f"Error: {cell_center} -> {e.stderr}"

#     except Exception as ex:
#         # Handle unexpected errors
#         return f"Unexpected error: {cell_center} -> {str(ex)}"

# def scan_cells(cell_centers):
#     """
#     Run all scraper commands in parallel using threading.
#     """
#     results = []
#     with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
#         # Submit tasks to the executor
#         future_to_cell = {executor.submit(run_scraper, cell): cell for cell in cell_centers}

#         # Process results as they complete
#         for future in as_completed(future_to_cell):
#             results.append(future.result())

#     return results

# for cell_center in cell_centers:
#         scraper_command = f"{PATH}/{SCRAPER_NAME} -depth {SCRAPER_DEPTH} -zoom {SCRAPER_ZOOM} -geo {cell_center[0]},{cell_center[1]} -input {PATH}/{INPUT_NAME} -results {RESULTS_FOLDER}/{str(uuid.uuid4())}.csv -exit-on-inactivity 10m"
#         # Run the scraper
#         os.system(scraper_command)

# def main():
#     # Get cell centers to scan
#     cell_centers = get_cell_centers()

#     # Scan
#     scan_cells(cell_centers)

#     # Extract results
    
#     # Send results to server
#     pass

# if __name__ == "__main__":
#     main()