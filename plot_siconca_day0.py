#!/usr/bin/env python3
"""
plot_siconca_day0.py
Plot sea ice concentration for a single day (day 0) from the OSISAF SICONCA dataset.
"""

import xarray as xr
import matplotlib.pyplot as plt

def main():
    # Path to the NetCDF file
    ds_path = "/home/arjuna_scagnetto/icenet/data/osisaf/north/siconca/2023.nc"
    # Day index to plot (0-based)
    day_index = 0

    # Open the dataset
    ds = xr.open_dataset(ds_path)
    # Select the sea ice concentration for the specified day and convert to percent
    ice = ds.ice_conc.isel(time=day_index) * 100.0
    # Load coordinates
    lon = ds.lon
    lat = ds.lat

    # Plotting
    plt.figure(figsize=(10, 8))
    pcm = plt.pcolormesh(lon, lat, ice, shading='auto', cmap='viridis')
    plt.colorbar(pcm, label=f"Ice concentration ({ds.ice_conc.units})")
    # Extract date for title
    date = str(ds.time.values[day_index])[:10]
    plt.title(f"Sea Ice Concentration on {date}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()