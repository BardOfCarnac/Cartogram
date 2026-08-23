#!/usr/bin/env python3
"""Build the Night City map-aligned heightfield from a source DEM tile.

Usage:
    python tools/build_night_city_heightfield.py \
        --dem /path/to/USGS_1_n36w121.tif \
        --registration data/night-city-2045/terrain/registration.json \
        --out data/night-city-2045/terrain/heightfield.tif

The output grid is exactly the Night City map pixel grid. Existing Night City
geometry can therefore sample elevation with the same integer (x, y) pixel
coordinates it already uses.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import rasterio
from pyproj import Transformer


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--dem", required=True, type=Path)
    p.add_argument("--registration", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    reg = json.loads(args.registration.read_text())

    width = int(reg["map_image"]["width_px"])
    height = int(reg["map_image"]["height_px"])
    ll = reg["registration"]["pixel_center_to_lonlat"]

    # Pixel-center coordinates in the Night City map grid.
    yy, xx = np.mgrid[0:height, 0:width]
    lon = (
        ll["lon"]["x_coeff"] * xx
        + ll["lon"]["y_coeff"] * yy
        + ll["lon"]["constant"]
    )
    lat = (
        ll["lat"]["x_coeff"] * xx
        + ll["lat"]["y_coeff"] * yy
        + ll["lat"]["constant"]
    )

    with rasterio.open(args.dem) as src:
        transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
        sx, sy = transformer.transform(lon.ravel(), lat.ravel())

        # Nearest-neighbour sampling is deliberate here. The aligned raster is a
        # lookup surface tied to the map geometry, not a cartographic resampling
        # product. Interpolation can be added explicitly later if desired.
        coords = zip(sx.tolist(), sy.tolist())
        values = np.fromiter(
            (float(v[0]) for v in src.sample(coords, indexes=1)),
            dtype=np.float32,
            count=width * height,
        ).reshape(height, width)

    transform_values = reg["registration"]["geotiff_affine_corner_transform"]
    transform = rasterio.Affine(*transform_values)

    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:4326",
        "transform": transform,
        "compress": "deflate",
        "predictor": 3,
        "nodata": np.nan,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(args.out, "w", **profile) as dst:
        dst.write(values, 1)
        dst.update_tags(
            source_dem=args.dem.name,
            coordinate_rule="Night City map pixel (x,y) samples heightfield pixel (x,y)",
            vertical_units="metres",
            working_sea_level_m="0",
        )

    finite = values[np.isfinite(values)]
    print(f"wrote {args.out}")
    print(f"grid: {width} x {height}")
    if finite.size:
        print(f"elevation range: {finite.min():.2f} .. {finite.max():.2f} m")


if __name__ == "__main__":
    main()
