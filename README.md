# Cartogram

Cartogram is the map engine and spatial-data codebase behind **Spaciel**.

The project is intended to describe, render, query, and edit maps independently of any one setting. Night City 2045 is the first working dataset and test case, not the definition of the engine.

## Core responsibilities

- map geometry and coordinate systems
- road topology and routing graphs
- areas, boundaries, and containment
- places and spatial entities
- reusable overlays attached to points, roads, and areas
- authoring and inspection tools

Product-specific systems such as accounts, campaigns, inventories, encounter rules, and the Spaciel interface should remain outside Cartogram unless they become genuinely reusable spatial primitives.

## Current Night City work

Existing generated assets include:

- `night_city_2045_road_graph_v12.geojson` — extracted and attributed road graph
- `night_city_buildings_wireframe_3d.json` — building placements and deduplicated 3D wireframe geometry extracted from the SketchUp source model

These generated datasets are being migrated into the repository. Official Cyberpunk RED PDFs and other third-party reference assets are **reference sources, not repository assets**, unless redistribution rights are explicitly established.

See `docs/` and `data/night-city-2045/` as the repository is populated.
