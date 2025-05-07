from icenet.data.processors.era5 import IceNetERA5PreProcessor
import pandas as pd
import os
import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


logging.basicConfig(
    filename='processing_debug.log',  # nome del file di log
    filemode='w',                     # modalità ('w' sovrascrive, 'a' aggiunge)
    level=logging.DEBUG,              # livello di log
    format='%(asctime)s - %(levelname)s - %(message)s'
)



processing_dates = dict(
    train=[pd.to_datetime(el) for el in pd.date_range("2020-01-01", "2020-03-31")],
    val=[pd.to_datetime(el) for el in pd.date_range("2020-04-03", "2020-04-23")],
    test=[pd.to_datetime(el) for el in pd.date_range("2020-04-01", "2020-04-02")],
)
processed_name = "tutorial_api_data"

pp = IceNetERA5PreProcessor(
    ["uas", "vas"],                 
    ["zg500", "zg250"],      
    processed_name,
    processing_dates["train"],
    processing_dates["val"],
    processing_dates["test"],
    linear_trends=tuple(),
    north=True,
    south=False,
    file_filters=["latlon_"]
)

base_path = os.path.abspath(os.path.dirname(__file__))
source_data_path = os.path.join(base_path, "data", "era5", "north")

pp._source_data = source_data_path
print("Using source data path:", source_data_path)

# Detailed check

for var in ["uas", "vas", "zg500", "zg250"]:
    expected_path = os.path.join(pp._source_data, var)
    logging.debug("Checking existence of path: %s (Exists: %s)", expected_path, os.path.exists(expected_path))

pp.init_source_data(lag_days=1)
pp.process()

