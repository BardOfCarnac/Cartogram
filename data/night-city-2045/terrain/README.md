# Night City 2045 terrain reference

This directory contains the **canonical terrain inputs and compact terrain data** currently used to register Night City 2045 geometry against the Morro Bay-area elevation model.

The goal is to make the terrain work available to future Cartogram/Spaciel conversations without carrying forward every experimental cut, fill, terrace, or alignment attempt.

## Canonical files

- `registration.json` — exact Night City map-pixel to longitude/latitude registration. The working map grid is 780 × 1200 px at approximately 17.826 m/px.
- `terrain-source.json` — source DEM, grid, vertical datum, and regeneration notes.
- `terrain-contours-100m.geojson` — compact LiDAR/DEM-derived terrain reference in Night City pixel coordinates. This is intended for quick project-wide inspection, not precise road grading.
- `city-footprint.geojson` — current approved **single continuous construction footprint**. Internal district borders are deliberately not holes.
- `water-mask.geojson` — current water/ocean/canal geometry derived from the working water mask.
- `major-grade-routes.json` — the two principal route traces used during early grade diagnostics (north–south trunk and east branch). The full road graph elsewhere in the repository remains authoritative for road geometry.
- `tools/build_night_city_heightfield.py` — regenerates the full 780 × 1200 aligned elevation raster from the upstream USGS DEM and `registration.json`.

## Terrain data strategy

The original working source tile is `USGS_1_n36w121.tif`. It is a large upstream USGS terrain tile, so it is **not vendored into this repository**. The full map-aligned float raster is likewise treated as a generated dataset rather than the canonical source of truth.

For quantitative work, regenerate it with:

```bash
python tools/build_night_city_heightfield.py \
  --dem /path/to/USGS_1_n36w121.tif \
  --registration data/night-city-2045/terrain/registration.json \
  --out data/night-city-2045/terrain/heightfield.tif
```

The resulting raster is exactly 780 × 1200 and obeys the core integration rule:

> A Night City geometry point `(x, y)` samples terrain elevation at heightfield pixel `(x, y)`.

Working sea level is `0 m`. The source-aligned raster observed in the current work ranged from approximately 0 m to 623 m.

`terrain-contours-100m.geojson` is committed as a lightweight, directly searchable representation of the real terrain so future work can understand the broad landscape without first regenerating the raster.

## Registration

The current registration is trace-derived from the Morro Bay / CA-1 / CA-41 correspondence. The registered Night City footprint is approximately 13.90 km × 21.39 km. The geographic anchor is the CA-1 / CA-41 junction at approximately `35.380111, -120.85625`. `registration.json` contains the exact affine coefficients.

## What is deliberately NOT canonical

Do **not** treat old terrain experiments as source data. Earlier files involving district-separated masks, independently stretched masks, flat +265 m slabs, road-corridor cuts, successive cut/fill surfaces, and preliminary terrace tests were exploratory and are intentionally omitted.

Current terrain design direction is:

1. use one continuous city construction footprint;
2. keep water tied to sea level (`0 m`);
3. derive city surface heights from the real landscape rather than floating the entire city high above it;
4. allow buildings/blocks to become local flat terraces;
5. let roads and especially bridges/elevated links carry useful gradient between terraces;
6. preserve surrounding real terrain outside the engineered city footprint.

See `docs/night-city-2045-terrain-status.md` for the current modelling status and next questions.

## Reference-map rights

The official Cyberpunk RED map/PDF and third-party map imagery remain **reference sources, not repository assets**, unless redistribution rights are established. The registration, masks, road geometry and terrain derivatives in this directory are the reusable Cartogram data produced from that work.
