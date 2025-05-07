from icenet.data.processors.era5 import IceNetERA5PreProcessor
from icenet.data.processors.meta import IceNetMetaPreProcessor
from icenet.data.processors.osi import IceNetOSIPreProcessor

import pandas as pd

processing_dates = dict(
    train=[pd.to_datetime(el) for el in pd.date_range("2020-01-01", "2020-03-31")],
    val=[pd.to_datetime(el) for el in pd.date_range("2020-04-03", "2020-04-23")],
    test=[pd.to_datetime(el) for el in pd.date_range("2020-04-01", "2020-04-02")],
)
processed_name = "tutorial_api_data"

pp = IceNetERA5PreProcessor(
    ["uas", "vas"],                 # Absolute normalised variables
    ["zg500", "zg250"],      # Variables defined as deviations from an aggregated norm
    processed_name,
    processing_dates["train"],
    processing_dates["val"],
    processing_dates["test"],
    linear_trends=tuple(),
    north=True,
    south=False
)

"""osi = IceNetOSIPreProcessor(
    ["siconca"],                    # Absolute normalised variables
    [],                             # Variables defined as deviations from an aggregated norm
    processed_name,
    processing_dates["train"],
    processing_dates["val"],
    processing_dates["test"],
    linear_trends=tuple(),
    north=True,
    south=False
)"""

"""meta = IceNetMetaPreProcessor(
    processed_name,
    north=True,
    south=False
)
"""
pp.init_source_data(
    lag_days=1,
)
pp.process()

osi.init_source_data(
    lag_days=1,
)
osi.process()

meta.process()
