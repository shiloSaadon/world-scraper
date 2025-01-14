import os

# Current path where main.py
PATH = "./src"
#  The scraper binary code 
SCRAPER_NAME = "google_maps_scraper"
# File with queries to scrape
INPUT_NAME = "input.txt"
# Path for the results
RESULTS_FOLDER = f'{PATH}/results'
# The max amount of scrapping processes
MAX_THREADS=10
# The max number of queries for the scraper
QUERIES_COUNT = int(os.getenv("QUERIES_COUNT") if os.getenv("QUERIES_COUNT") else 300)
# Process and upload in batches
QUERIES_BATCH_COUNT = int(os.getenv("QUERIES_BATCH_COUNT") if os.getenv("QUERIES_BATCH_COUNT") else 25)