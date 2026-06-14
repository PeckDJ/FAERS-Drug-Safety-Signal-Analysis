"""Download and unzip FAERS quarterly ASCII data files from the FDA.

The FDA serves each quarter as a single zip at a predictable URL:

    https://fis.fda.gov/content/Exports/faers_ascii_<YEAR>q<Q>.zip

e.g. https://fis.fda.gov/content/Exports/faers_ascii_2024q1.zip

If a URL 404s, the quarter may not be published yet, or the path may have
changed. The canonical landing page (links move around over time) is:
    https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/fda-adverse-event-monitoring-system-aems-latest-quarterly-data-files

Inside each zip, the ASCII tables live under an ascii/ folder and are named
like DEMO24Q1.txt, DRUG24Q1.txt, REAC24Q1.txt, OUTC24Q1.txt — pipe-style
records delimited by '$'.

Usage:
    python -m src.download_faers
"""

import sys
import zipfile
from io import BytesIO

import requests

from .config import DATA_RAW, QUARTERS

BASE_URL = "https://fis.fda.gov/content/Exports/faers_ascii_{year}q{q}.zip"


def quarter_url(year: int, q: int) -> str:
    return BASE_URL.format(year=year, q=q)


def download_quarter(year: int, q: int) -> None:
    """Download one quarter and extract its ASCII tables into data/raw/<year>q<q>/."""
    dest = DATA_RAW / f"{year}q{q}"
    if dest.exists() and any(dest.glob("*.txt")):
        print(f"  [skip] {year}Q{q} already present at {dest}")
        return

    url = quarter_url(year, q)
    print(f"  [get ] {url}")
    resp = requests.get(url, timeout=300, stream=True,
                        headers={"User-Agent": "faers-signal-analysis/0.1"})
    if resp.status_code != 200:
        print(f"  [warn] {year}Q{q} returned HTTP {resp.status_code} — "
              f"may not be published yet. Skipping.")
        return

    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(BytesIO(resp.content)) as zf:
        for member in zf.namelist():
            # FAERS zips nest the tables under 'ascii/' (or 'ASCII/').
            name = member.split("/")[-1]
            if name.lower().endswith(".txt"):
                with zf.open(member) as src, open(dest / name, "wb") as out:
                    out.write(src.read())
    n = len(list(dest.glob("*.txt")))
    print(f"  [ok  ] {year}Q{q}: extracted {n} tables to {dest}")


def main() -> int:
    print(f"Downloading {len(QUARTERS)} quarter(s) to {DATA_RAW}")
    for year, q in QUARTERS:
        download_quarter(year, q)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
