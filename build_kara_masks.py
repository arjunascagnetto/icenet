#!/usr/bin/env python3
"""
build_kara_masks.py

Generate Kara-Sea-only mask files for IceNet:

  data/masks/n/masks/active_grid_cell_mask_01.npy … 12
  data/masks/n/masks/land_mask.npy

Usage:
  python build_kara_masks.py [--raw-dir data/era5] [--hemi north]
"""
import os
import glob
import argparse
import xarray as xr
import numpy as np

def parse_args():
    p = argparse.ArgumentParser(
        description="Build Kara Sea masks for IceNet"
    )
    p.add_argument(
        "--raw-dir",
        default="data/era5",
        help="Root directory containing raw ERA5 .nc files"
    )
    p.add_argument(
        "--hemi",
        choices=["north","south"],
        default="north",
        help="Hemisphere (affects mask folder: n or s)"
    )
    p.add_argument("--lat-min", type=float, default=65.0,
                   help="Latitude min for Kara Sea")
    p.add_argument("--lat-max", type=float, default=80.0,
                   help="Latitude max for Kara Sea")
    p.add_argument("--lon-min", type=float, default=60.0,
                   help="Longitude min for Kara Sea")
    p.add_argument("--lon-max", type=float, default=100.0,
                   help="Longitude max for Kara Sea")
    return p.parse_args()

def main():
    args = parse_args()
    # find a sample file to grab lat/lon
    candidates = glob.glob(os.path.join(args.raw_dir, "*", "*.nc"))
    if not candidates:
        raise RuntimeError(f"No .nc files under {args.raw_dir}")
    sample = candidates[0]
    ds = xr.open_dataset(sample)
    # detect lat/lon coords
    lat = ds.coords.get("lat") or ds.coords.get("latitude")
    lon = ds.coords.get("lon") or ds.coords.get("longitude")
    if lat is None or lon is None:
        raise RuntimeError("Couldn't find lat/lon coords in sample file")
    # build mask, True inside your box
    mask2d = (
        (lat >= args.lat_min) & (lat <= args.lat_max) &
        (lon >= args.lon_min) & (lon <= args.lon_max)
    ).values
    # target folder
    hemi_char = "n" if args.hemi == "north" else "s"
    mask_dir = os.path.join("data", "masks", hemi_char, "masks")
    os.makedirs(mask_dir, exist_ok=True)
    # write monthly masks
    for m in range(1, 13):
        fn = os.path.join(mask_dir, f"active_grid_cell_mask_{m:02d}.npy")
        np.save(fn, mask2d)
        print("Wrote", fn)
    # write land mask (same array)
    land_fn = os.path.join(mask_dir, "land_mask.npy")
    np.save(land_fn, mask2d)
    print("Wrote", land_fn)

if __name__ == "__main__":
    main()
