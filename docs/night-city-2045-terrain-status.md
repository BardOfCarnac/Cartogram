# Night City 2045 terrain — current modelling status

This note records the current state of the terrain work without promoting every exploratory raster to repository data.

## Settled geometry

- Night City map grid: **780 × 1200 px**.
- Approximate scale: **17.826 m/px**.
- Approximate registered footprint: **13.90 km × 21.39 km**.
- Geographic anchor used during registration: **CA-1 / CA-41 junction**, approximately `35.380111, -120.85625`.
- Current city construction footprint is **one continuous solid footprint**. Internal district boundary lines must never create terrain gaps/ridges.
- Water/canal areas remain void/low areas tied to the working **0 m sea-level datum**.

## Terrain interpretation

The first instinct was to keep most of Night City above the Morro Bay landscape to avoid large cuts. A later cut/fill comparison showed that this was over-cautious:

- about **85%** of the then-current city surface lay above the real landscape;
- about **15%** lay below it;
- the average city-surface offset was roughly **+65 m**;
- about **58%** of the city footprint was more than **50 m above** the underlying landscape.

Those figures came from an exploratory graded/terraced surface and should be treated as diagnostics, not as a canonical target surface. Their main implication is robust: **the city can probably be lowered substantially before excavation becomes the dominant problem**.

## Grade grammar under test

Current working design limits are deliberately conservative:

- building pads / plazas: approximately flat (0–2%);
- major roads: target ≤ **6%**;
- ordinary streets: target ≤ **8%**;
- steeper local streets/ramps may occasionally reach 8–12% or somewhat more;
- bridges/elevated roads are useful gradient carriers because they can change elevation independently of the ground beneath them;
- open land, embankments, cut slopes and retaining walls can absorb much sharper local transitions than roads or building pads.

An exploratory pass using those limits suggested the road network can carry the broad city-scale descent without requiring extreme grades. The exact parcel/road classification still needs to be derived from clean building and road geometry rather than inferred from atlas linework.

## Current next steps

1. Compare the city surface and real terrain as a **signed difference map** to locate the largest natural drops/cuts beneath each part of the city.
2. Test global downward shifts (for example 25 m / 50 m / 75 m) and compare fill versus cut volume and edge severity.
3. Make a district-by-district / structural **height-change capacity map**: protect dense flat blocks, identify terraces, slope-tolerant ground, bridge/elevated corridors, and good places for retaining/cut transitions.
4. Use the building model to create genuine local flat pads instead of inferring parcels from rendered map linework.
5. Solve the final terrain as a constrained surface that joins those pads and road grades while preserving the real landscape outside the city footprint.

## Important warning

Do not resurrect earlier district-separated terrain masks or independently stretch masks to fit. The approved terrain operation starts from the continuous `city-footprint.png` mask and the registration in `terrain/registration.json`.
