# Night City 2045 dataset

Night City 2045 is Cartogram's first working map dataset and test case.

## Canonical generated files

### `roads.geojson`

Target for the current `night_city_2045_road_graph_v12.geojson` dataset.

Known current metadata:

- GeoJSON `FeatureCollection`
- clean-map source image: 5175 × 7966 px
- coordinate system: clean-map image pixels, origin top-left, x right, y down
- 1,681 nodes
- 2,207 road edges
- 567 major edges
- 1,640 local edges
- 33 graph components
- largest component: 1,571 nodes
- street attribution includes registered district-map sources, accepted road names, graph edge indexes, review queues, corrections, and registration transforms

The file should be migrated byte-for-byte from the current generated asset rather than reconstructed from search snippets.

### `buildings-wireframe-3d.json`

Target for the current `night_city_buildings_wireframe_3d.json` dataset.

Known current metadata:

- source model: `Night+City2045_2 (1).skp`
- source layer: `buildings`
- 16,383 building placements
- 365,356 unique line segments
- 408,973 source line segments before deduplication
- contains map-space and metre-space coordinate metadata

The file should likewise be migrated from the original generated asset rather than reconstructed.

## Reference assets

The exact clean master image used by the road graph should be preserved in the development/reference archive because its pixel coordinate system defines the graph. Do not add copyrighted reference artwork to the public repository without checking redistribution rights.

## Naming

Once migrated, prefer stable canonical filenames (`roads.geojson`, `buildings-wireframe-3d.json`) and let Git history carry version numbers such as `v12`.
