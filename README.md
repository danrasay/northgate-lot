# S Northgate Ave — lot study

Feasibility study for a vacant 0.58-acre flag lot on S Northgate Ave,
Portland OR 97219 (Multnomah County tax account R547474), adjoining the
owners' residence.

Everything here is static — no build step, no dependencies to install for
viewing.

## Look at it

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. The hub page links the two interactive
models and both PDFs.

Opening `index.html` directly from the filesystem also works, though a local
server is tidier.

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | Hub page. The contour hero is drawn from the same elevation model the 3D studies use. |
| `models/massing.html` | Four development options (A–D) on the hillside, toggleable. |
| `models/driveway.html` | Four driveway alignments up the flag pole, with grades computed live from the geometry. |
| `docs/Development_Options_Report.pdf` | Nine-page written study. |
| `docs/Options_One_Pager.pdf` | Landscape comparison matrix. |
| `tools/fetch_dem.py` | Pulls USGS 3DEP lidar elevations into `data/dem_grid.json`. |
| `tools/build_report.py`, `tools/build_onepager.py` | Regenerate the PDFs (`pip install reportlab`). |

## The next real task

The terrain in both models is an approximation anchored to a labeled 340-ft
contour and the owners' description. Replacing it with measured elevations is
the highest-value improvement available:

```bash
python3 tools/fetch_dem.py     # writes data/dem_grid.json
```

Then drive `elev()` in both models from that grid. `CLAUDE.md` carries the
full brief, including the coordinate registration and the interpolation
approach.

This fetch fails inside the Claude.ai sandbox — its egress proxy blocks
`epqs.nationalmap.gov` — but runs fine anywhere with ordinary network access.

## Publishing

The site is plain static files, so any static host works. For GitHub Pages:

```bash
git remote add origin git@github.com:USER/REPO.git
git push -u origin main
```

Then in the repository settings, under Pages, publish from `main` at the root.
The study lands at `https://USER.github.io/REPO/`.

**Before publishing anywhere public, consider what should stay private.** This
repo names a specific parcel under contract and discusses the owners'
financial reasoning. A private repository, or a host behind a login, is the
safer default. GitHub Pages sites built from private repos are public unless
you are on a plan that supports private Pages.

## Standing caveats

Planning-level work for the owners' internal decisions. Not legal, tax,
investment, or engineering advice. Costs are ranges of roughly ±25%, grades are
computed over approximate terrain, and zoning interpretations need confirmation
with the City of Portland. The preliminary title report is still outstanding,
including an easement the seller disclosed but never attached.
