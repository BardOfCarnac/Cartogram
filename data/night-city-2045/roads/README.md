# Night City 2045 roads

This directory is the home for the canonical Night City 2045 road dataset used by Cartogram/Spaciel.

## Coordinate frame

The current road work uses the clean 5175 × 7966 map image coordinate system:

- origin: top-left
- +x: right
- +y: down
- no geographic reprojection has been applied

This preserves direct overlay compatibility with the working master map.

## Canonical graph

The current canonical graph is `night_city_2045_road_graph_v12.geojson`.

Its metadata records:

- 1,681 road nodes
- 2,207 road edges
- 1,640 local edges
- 567 major edges
- road-width measurements on edges
- audited street-name attribution for a substantial portion of the city

The graph distinguishes two road classes for the current renderer: `local` and `major`.

## Display reconstruction

The clean display-road experiment reached v10 before repository migration. The useful decisions from that work are now captured in `config/night-city-2045-roads.json` and `tools/render_night_city_roads.py`:

- local roads: 9 px grey stroke
- major roads: 19 px yellow stroke
- no horizontal, vertical, or angle snapping
- graph geometry remains authoritative
- road segments use clean vector strokes
- junctions are rendered with one node disc rather than stacked round caps
- display cleanup must not modify the routing/source graph

The earlier raster-mask repair experiments are not canonical and should not be treated as source geometry.

## Source assets

Official Cyberpunk RED PDFs/maps and other third-party source artwork are reference material only and are not to be committed here unless redistribution rights are established.

Derived graph data and renderer output may be stored here according to the project's licensing/attribution policy.
