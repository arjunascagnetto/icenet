import numpy as np
import pandas as pd
import os
import random

# We also set the logging level so that we get some feedback from the API
import logging
logging.basicConfig(level=logging.INFO)

from icenet.data.sic.mask import Masks
#from icenet.data.interfaces.cds import ERA5Downloader
#from icenet.data.sic.osisaf import SICDownloader

masks = Masks(north=True, south=False)
masks.generate(save_polarhole_masks=True)
