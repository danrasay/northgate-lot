# CLAUDE.md — S Northgate Ave lot study

Context for Claude Code sessions working in this repo.

## What this is

A feasibility study for a vacant 0.58-acre (25,281 sq ft) **flag lot** on
S Northgate Ave, Portland OR 97219 (Multnomah County tax account **R547474**),
adjoining the owners' existing residence. The owners are evaluating development
options: rental income, space for visiting family, and lifestyle uses
(workshop, sport court).

Deliverables are a written study, a one-page comparison, and two interactive
3D massing models.

## Site facts already established

- **Jurisdiction: City of Portland** (annexed). PortlandMaps shows
  "Portland / Multnomah" and **City Council District 4** — county rules do
  not apply. This is the pivotal regulatory fact.
- **Zoning R20**, no `c` / `p` / `z` overlay letters observed.
- **Flag geometry (corrected — see Data provenance)**: the 15-ft × 141-ft pole
  is on the **north** side of the flag body, meeting **S Northgate Ave's
  cul-de-sac** (bulb R=28.5 ft, per the plat) — not a straight street frontage.
  The owners' home (**11520 S Elysium Pl**) sits northeast of the flag body,
  across the shared taxlot line. **S Elysium Pl**, not S Powers Ct, is the
  real cross street (S Powers Ct does not border this site — that was an
  error reading the DOGAMI annotation). Ground eases away southwest toward
  Terwilliger and Tryon Creek.
- **Seller / current owner of record of the flag lot**: the neighbor at
  **11605 S Elysium**. Flag lot is Partition Plat 2004-35, Lot 3.
- **Terrain**: cul-de-sac apron ≈336 ft; flag body ≈336–387 ft; the owners'
  home sits ≈392–403 ft. USGS 3DEP lidar, live in both models.
- **Driveway grade — corrected and materially worse than earlier estimated**:
  the real pole easement (apron to where it enters the flag body) averages
  **~22%** with a sustained pinch near **~37%** — both over Portland's ~20%
  driveway ceiling, not just borderline. See `models/driveway.html` Option 1.
  Cutting the profile (Option 2) brings the *average* back under the cap but
  not the pinch. Only extending the drive past the legal easement onto the
  owner's own land in the flag body (Options 3/4) gets a genuinely gentle
  (~7–8%) grade — at the cost of a much longer run.
- **DOGAMI shallow landslide susceptibility: LOW** on both parcels.
- **Utilities**: public water and sewer available at the boundary (not
  connected; water hook-up charge unknown); electric, gas, phone, internet
  at the boundary. No soil tests, no known contamination.
- **Survey**: Record of Survey 68582, filed May 2023 (Centerline Concepts).
  The parcel was assembled from West Palatine Ridge lots, part of Palatine
  Hill Block 63, a partition parcel, and a 1947 street vacation.

## Data provenance

The site facts above (street/cul-de-sac geometry, addresses, seller, plat
number, driveway grade) were corrected in 2026-07 against real GIS pulls,
replacing earlier readings of the owner's annotated DOGAMI map:

| Data | Source |
|---|---|
| Terrain (29×29 grid, `tools/fetch_dem.py`) | USGS 3DEP EPQS `epqs.nationalmap.gov/v1/json` |
| Taxlots, building footprints, street centerlines, 2019 lidar contours | PortlandMaps ArcGIS (`Public/Taxlots`, `Public/Basemap_Color_Buildings`, `Public/CGIS_Layers` MapServer layers) |
| Aerial photo (`data/aerial.jpg`) | PortlandMaps Summer 2024 orthophoto |

All of the above (except the freshly-fetched DEM grid) live in
`data/site_vectors.json`, fetched at runtime by both models alongside
`data/dem_grid.json`. This still isn't a substitute for the preliminary
title report (open item below) — it resolves the street/geometry confusion
but not the undisclosed easement.

## Four development options

| | Option | Note |
|---|---|---|
| A | Rental house (~2,400 sf) + detached ADU (~800 sf) | recommended baseline |
| B | Duplex (~3,000 sf), hold both units | best pure yield |
| C | Single rental house | simplest build |
| D | Consolidate lots into a compound (ADU + workshop + sport court) | **only lawful short-term-rental route** — Portland Type A permits require the operator to live on the same tax lot |

## Repo map

```
index.html            hub page; contour hero drawn from its own analytic elevation fn (not yet on real data — see below)
models/massing.html   4 site options (A–D), real taxlots/buildings/streets/contours, AERIAL/PLAN toggle
models/driveway.html  4 pole driveway options on the real easement, grades computed live
docs/*.pdf            written study + one-page comparison
tools/fetch_dem.py    USGS 3DEP elevation fetch -> data/dem_grid.json
tools/build_*.py      reportlab generators for the two PDFs
data/dem_grid.json    terrain grid (29x29, fetched by tools/fetch_dem.py)
data/site_vectors.json  real taxlots, buildings, streets, cul-de-sac, driveway pole, 2ft/10ft contours (see Data provenance)
data/aerial.jpg        2024 PortlandMaps orthophoto, pre-aligned to site_vectors.json's `ext`
```

## Recently completed

- **Lidar terrain rebuild** (both models now fetch `data/dem_grid.json` at
  runtime and sample it via Catmull-Rom bicubic interpolation — no more
  analytic terrain).
- **GIS data correction** (2026-07): replaced DOGAMI-map-derived approximate
  geometry with real PortlandMaps/lidar-survey data across both models. See
  "Data provenance" above and the corrected site facts. This also resolved
  open item 4 below (legal-lot confirmation) via the plat number.

## Open work, highest value first

1. **Preliminary title report**, when the owners receive it. The seller
   disclosed an easement beyond utility/drainage but never attached the
   instrument. Fold findings into the report and revise the risk register.
   The GIS data correction above did not touch this — it fixed the street/
   geometry confusion, not the undisclosed easement.
2. **`index.html`'s hero contour** still uses its own standalone analytic
   `elevAbs()`, never converted to fetch `data/dem_grid.json` like the two
   models. Low priority (decorative hero, not a finding), but it now
   describes different, less accurate terrain than either model.

## Conventions

- **Keep the elevation function identical across both models.** They must
  describe the same ground. When the lidar rebuild lands, update both.
- Local coordinates: **+x north, +z east, feet.** The owner's center pin
  (45.4413056, -122.6696944) is local (-2.5, 170).
- Palette: forest `#1F3D2B`, moss `#4A6B52`, sand `#EFE9DD`,
  copper `#B0713A`, ink `#2B2B28`. Copper is reserved for 10-ft index
  contours and the active/primary accent — do not spend it elsewhere.
- Type: Space Grotesk (display), IBM Plex Mono (data and captions).
- Models are single-file, vanilla Three.js r128 from cdnjs, no build step.
  No browser storage APIs.

## Tone for anything user-facing

Planning-level, honest about uncertainty. Every cost is a range, every
grade is labeled as computed over approximate terrain. Nothing here is
legal, tax, engineering, or investment advice, and the documents say so.
When the geometry produces an inconvenient finding, surface it rather
than smoothing it over — that is how the driveway grade cap issue was
caught.
