import numpy as np
import pandas as pd
import os
import random

# We also set the logging level so that we get some feedback from the API
import logging
logging.basicConfig(level=logging.INFO)

#from icenet.data.sic.mask import Masks
#from icenet.data.interfaces.cds import ERA5Downloader
from icenet.data.sic.osisaf import SICDownloader

#masks = Masks(north=True, south=False)
#masks.generate(save_polarhole_masks=True)

sic = SICDownloader(
    dates=[
        pd.to_datetime(date).date()     # Dates to download the variable data for
        for date in pd.date_range("2020-01-01", "2020-04-30", freq="D")
    ],
    delete_tempfiles=False,             # Whether to delete temporary downloaded files
    north=True,                        # Boolean: Whether to use mask for this region
    south=False,                         # Boolean: Whether to use mask for this region
    parallel_opens=False,               # Boolean: Whether to use `dask.delayed` to open and preprocess multiple files in parallel
)

sic.download()
