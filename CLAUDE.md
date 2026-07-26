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
- **Flag geometry**: the pole meets the S Northgate Ave public right of way;
  the flag body sits behind neighboring rear yards. The owners' home is
  **northeast** of the body. S Powers Ct wraps the south. Ground eases away
  southwest toward Terwilliger and Tryon Creek.
- **Terrain rises away from the street**, grades vary. Street at the pole is
  roughly 342–344 ft; the northeast rear reaches roughly 382 ft.
- **DOGAMI shallow landslide susceptibility: LOW** on both parcels.
- **Utilities**: public water and sewer available at the boundary (not
  connected; water hook-up charge unknown); electric, gas, phone, internet
  at the boundary. No soil tests, no known contamination.
- **Survey**: Record of Survey 68582, filed May 2023 (Centerline Concepts).
  The parcel was assembled from West Palatine Ridge lots, part of Palatine
  Hill Block 63, a partition parcel, and a 1947 street vacation.

## Four development options

| | Option | Note |
|---|---|---|
| A | Rental house (~2,400 sf) + detached ADU (~800 sf) | recommended baseline |
| B | Duplex (~3,000 sf), hold both units | best pure yield |
| C | Single rental house | simplest build |
| D | Consolidate lots into a compound (ADU + workshop + sport court) | **only lawful short-term-rental route** — Portland Type A permits require the operator to live on the same tax lot |

## Repo map

```
index.html            hub page; contour hero drawn from the shared elevation fn
models/massing.html   4 site options (A–D), toggleable
models/driveway.html  4 pole driveway options, grades computed live
docs/*.pdf            written study + one-page comparison
tools/fetch_dem.py    USGS 3DEP elevation fetch -> data/dem_grid.json
tools/build_*.py      reportlab generators for the two PDFs
data/                 dem_grid.json lands here
```

## Open work, highest value first

1. **Lidar terrain rebuild.** Run `python3 tools/fetch_dem.py`, then replace
   the analytic `elev()` in both models with sampling from `data/dem_grid.json`
   using Catmull-Rom bicubic interpolation. Set `REF = elevAbs(-55, 0)` (street
   at the pole) so scene geometry stays near y=0. Update the contour ramp range,
   the header badge to "USGS 3DEP lidar terrain," the legend numbers, and make
   the EL tick labels dynamic. **This fetch failed in the Claude.ai sandbox
   because of its egress proxy — it should work fine here.**
2. **Re-verify driveway grades** after the rebuild. On the current approximate
   terrain, Option 1 (follow natural grade) computes past Portland's ~20%
   driveway ceiling; a shallower real pole could make it viable again.
3. **Preliminary title report**, when the owners receive it. The seller
   disclosed an easement beyond utility/drainage but never attached the
   instrument. Fold findings into the report and revise the risk register.
4. **Legal-lot confirmation** — more than one lot of record would improve
   every option.

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
