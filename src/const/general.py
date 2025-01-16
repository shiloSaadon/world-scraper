import os

PATH = "./src"

config = {
    "PATH": PATH,
    # Current path where main.py
    #  The scraper binary code 
    "SCRAPER_NAME": "google_maps_scraper",
    # File with queries to scrape
    "INPUT_NAME": "input.txt",
    # Path for the results
    "RESULTS_FOLDER": f'{PATH}/results',
    # The max amount of scrapping processes
    "MAX_THREADS":10,
    # The max number of queries for the scraper
    "QUERIES_COUNT": int(os.getenv("QUERIES_COUNT") if os.getenv("QUERIES_COUNT") else 300),
    # Process and upload in batches
    "QUERIES_BATCH_COUNT": int(os.getenv("QUERIES_BATCH_COUNT") if os.getenv("QUERIES_BATCH_COUNT") else 25),
    # instance running the test
    "INSTANCE_ID": os.getenv("INSTANCE_ID") if os.getenv("INSTANCE_ID") else "localhost",
    # identifier of the run
    "RUN_ID": os.getenv("RUN_ID") if os.getenv("RUN_ID") else "localhost",
    # number of hexagons per run
    "HEXAGON_COUNT": int(os.getenv("HEXAGON_COUNT") if os.getenv("HEXAGON_COUNT") else "5"),
    # max number of hexagons per run
    "MAX_HEXAGON_COUNT": int(os.getenv("MAX_HEXAGON_COUNT") if os.getenv("MAX_HEXAGON_COUNT") else "10")
}