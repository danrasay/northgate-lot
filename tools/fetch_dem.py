#!/usr/bin/env python3
"""
Fetch a USGS 3DEP lidar elevation grid for the S Northgate Ave flag lot
and save it as data/dem_grid.json.

This could not run in the Claude.ai sandbox (egress proxy blocks
epqs.nationalmap.gov). It runs fine from Claude Code on a normal machine.

    python3 tools/fetch_dem.py

Registration
------------
The owner's dropped pin at the center of the flag body is
45.4413056 N, 122.6696944 W. In the local model coordinate system used by
models/massing.html and models/driveway.html, that point is (x=-2.5, z=170),
where +x runs north and +z runs east, both in feet.

Output
------
data/dem_grid.json:
    {"x0","z0","dx","dz","nx","nz","e":[[...]], "meta":{...}}
    e[iz][ix] is elevation in FEET above sea level (NAVD88 per 3DEP).
"""

import json
import math
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# --- registration ------------------------------------------------------
LAT0, LON0 = 45.4413056, -122.6696944   # owner's center pin
CX, CZ = -2.5, 170.0                    # same point in local model feet

# --- sampling grid (local feet) ---------------------------------------
X0, Z0 = -190.0, -45.0
DX, DZ = 17.0, 17.25
NX, NZ = 21, 21                         # 441 points

ENDPOINT = "https://epqs.nationalmap.gov/v1/json"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "dem_grid.json")

_phi = math.radians(LAT0)
_m_lat = 111132.92 - 559.82 * math.cos(2 * _phi) + 1.175 * math.cos(4 * _phi)
_m_lon = 111412.84 * math.cos(_phi) - 93.5 * math.cos(3 * _phi)
FT_PER_DEG_LAT = _m_lat * 3.280839895
FT_PER_DEG_LON = _m_lon * 3.280839895


def to_latlon(x, z):
    """Local model feet -> (lat, lon). +x is north, +z is east."""
    return (LAT0 + (x - CX) / FT_PER_DEG_LAT,
            LON0 + (z - CZ) / FT_PER_DEG_LON)


def query(lat, lon, tries=3):
    url = f"{ENDPOINT}?x={lon:.7f}&y={lat:.7f}&units=Feet&wkid=4326"
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                value = float(json.load(resp).get("value"))
                if -50 < value < 15000:
                    return value
        except Exception:
            time.sleep(0.4 * (attempt + 1))
    return None


def main():
    probe = query(LAT0, LON0)
    if probe is None:
        sys.exit("Could not reach the USGS elevation service. Check network access.")
    print(f"center pin: {probe:.1f} ft")

    targets = [(ix, iz) for iz in range(NZ) for ix in range(NX)]
    coords = [to_latlon(X0 + ix * DX, Z0 + iz * DZ) for ix, iz in targets]

    grid = [[None] * NX for _ in range(NZ)]
    started = time.time()
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = pool.map(lambda c: query(*c), coords)
        for (ix, iz), value in zip(targets, results):
            grid[iz][ix] = value

    missing = sum(1 for row in grid for v in row if v is None)
    print(f"fetched {len(targets)} points in {time.time() - started:.0f}s "
          f"({missing} gaps)")

    guard = 0
    while missing and guard < 50:
        guard += 1
        for iz in range(NZ):
            for ix in range(NX):
                if grid[iz][ix] is None:
                    near = [grid[j][i]
                            for i, j in ((ix - 1, iz), (ix + 1, iz),
                                         (ix, iz - 1), (ix, iz + 1))
                            if 0 <= i < NX and 0 <= j < NZ and grid[j][i] is not None]
                    if near:
                        grid[iz][ix] = sum(near) / len(near)
        missing = sum(1 for row in grid for v in row if v is None)

    flat = [v for row in grid for v in row]
    print(f"elevation range: {min(flat):.1f} to {max(flat):.1f} ft")

    payload = {
        "x0": X0, "z0": Z0, "dx": DX, "dz": DZ, "nx": NX, "nz": NZ,
        "e": [[round(v, 1) for v in row] for row in grid],
        "meta": {
            "source": "USGS 3DEP via epqs.nationalmap.gov",
            "units": "feet",
            "pin_lat": LAT0, "pin_lon": LON0,
            "pin_local_x": CX, "pin_local_z": CZ,
            "axes": "+x north, +z east, feet",
            "fetched": time.strftime("%Y-%m-%d"),
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh)
    print(f"wrote {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
