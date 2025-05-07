import numpy as np
import pandas as pd
import os
import random

# We also set the logging level so that we get some feedback from the API
import logging
logging.basicConfig(level=logging.DEBUG)

#from icenet.data.sic.mask import Masks
from icenet.data.interfaces.cds import ERA5Downloader
#from icenet.data.sic.osisaf import SICDownloader

#masks = Masks(north=True, south=False)
#masks.generate(save_polarhole_masks=True)

era5 = ERA5Downloader(
    var_names=["zg", "uas", "vas", "tas"],      # Name of variables to download
    dates=[                                     # Dates to download the variable data for
        pd.to_datetime(date).date()
        for date in pd.date_range("2020-01-01", "2020-04-30", freq="D")
    ],
    delete_tempfiles=False,                     # Whether to delete temporary downloaded files
    levels=[[250, 500], None, None, None],      # The levels at which to obtain the variables for (e.g. for zg, it is the pressure levels)
    max_threads=64,                             # Maximum number of concurrent downloads
    north=True,                                # Boolean: Whether require data across northern hemisphere
    south=False,                                 # Boolean: Whether require data across southern hemisphere
    # NOTE: there appears to be a bug with the toolbox API at present (icenet#54)
    use_toolbox=False)                          # Experimental, alternative download method

#era5.download() 


era5.regrid()
era5.rotate_wind_data()
