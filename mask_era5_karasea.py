#!/usr/bin/env python3
"""
Quick & dirty Kara Sea mask for daily ERA5 netCDFs.

Usage:
  python mask_era5_karasea.py RAW_DIR OUT_DIR

  RAW_DIR: path to root of raw ERA5 daily netCDFs, e.g. data/era5
  OUT_DIR: path to write masked netCDFs, e.g. data/era5_karasea

The script will process variables: tas, uas, vas, zg at 250 & 500 hPa.
"""
import os
import sys
import glob
import argparse
import xarray as xr
import numpy as np

def parse_args():
    p = argparse.ArgumentParser(description="Mask ERA5 netCDFs to Kara Sea BBox.")
    p.add_argument('raw_dir', help='Root directory of raw ERA5 files')
    p.add_argument('out_dir', help='Directory to write masked files')
    p.add_argument('--lat-min', type=float, default=65.0, help='Latitude minimum')
    p.add_argument('--lat-max', type=float, default=80.0, help='Latitude maximum')
    p.add_argument('--lon-min', type=float, default=60.0, help='Longitude minimum')
    p.add_argument('--lon-max', type=float, default=100.0, help='Longitude maximum')
    return p.parse_args()

def mask_folder(in_base, out_base, lat_min, lat_max, lon_min, lon_max):
    os.makedirs(out_base, exist_ok=True)
    files = sorted(glob.glob(os.path.join(in_base, '*.nc')))
    if not files:
        print(f"[WARN] No files found in {in_base}")
    for fn in files:
        print(f"Masking {fn}")
        ds = xr.open_dataset(fn)
        # detect lat/lon coords
        if 'latitude' in ds.coords and 'longitude' in ds.coords:
            lat = ds.latitude
            lon = ds.longitude
        elif 'lat' in ds.coords and 'lon' in ds.coords:
            lat = ds.lat
            lon = ds.lon
        else:
            # fallback to any 2D coords
            lat = ds.coords.get('lat') or ds.coords.get('latitude')
            lon = ds.coords.get('lon') or ds.coords.get('longitude')
        mask = ((lat >= lat_min) & (lat <= lat_max) &
                (lon >= lon_min) & (lon <= lon_max))
        # apply mask to all data variables
        for v in ds.data_vars:
            ds[v] = ds[v].where(mask)
        outfn = os.path.join(out_base, os.path.basename(fn))
        ds.to_netcdf(outfn)
        ds.close()

def main():
    args = parse_args()
    vars2d = ['tas', 'uas', 'vas']
    levels = ['250', '500']  # for zg
    # process 2D vars
    for v in vars2d:
        in_dir = os.path.join(args.raw_dir, v)
        out_dir = os.path.join(args.out_dir, v)
        mask_folder(in_dir, out_dir,
                    args.lat_min, args.lat_max,
                    args.lon_min, args.lon_max)
    # process 3D zg
    for lev in levels:
        # try folder 'zg/250' or 'zg_250'
        sub1 = os.path.join(args.raw_dir, 'zg', lev)
        sub2 = os.path.join(args.raw_dir, f'zg_{lev}')
        if os.path.isdir(sub1):
            in_dir = sub1
        else:
            in_dir = sub2
        out_dir = os.path.join(args.out_dir, 'zg_' + lev)
        mask_folder(in_dir, out_dir,
                    args.lat_min, args.lat_max,
                    args.lon_min, args.lon_max)

if __name__ == '__main__':
    main()
