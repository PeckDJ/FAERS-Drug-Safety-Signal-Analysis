"""Central configuration for the FAERS signal-analysis pipeline.

Edit TARGET_DRUGS and QUARTERS to point the analysis at the drug class you
know best. Everything downstream reads from here.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"          # downloaded + unzipped FAERS files
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES = PROJECT_ROOT / "figures"

for _p in (DATA_RAW, DATA_PROCESSED, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Which quarters to analyse
# Format: (year, quarter). Add more for a larger, more stable signal base.
# Each quarter is a separate ~30-60 MB download from the FDA.
# ---------------------------------------------------------------------------
QUARTERS = [
    (2024, 1),
    (2024, 2),
    (2024, 3),
    (2024, 4),
]

# ---------------------------------------------------------------------------
# Target drug(s)
# Matching is case-insensitive substring matching against the FAERS `drugname`
# and `prod_ai` (active ingredient) fields. Use generic names where possible.
# Example below: a few common cardiovascular drugs. Swap in your own class.
# ---------------------------------------------------------------------------
TARGET_DRUG_LABEL = "Cardiovascular sample"
TARGET_DRUGS = [
    "atorvastatin",
    "rosuvastatin",
    "simvastatin",
]

# Only count the drug when it is the suspected cause, not an incidental
# concomitant medication. FAERS role codes: PS = primary suspect,
# SS = secondary suspect, C = concomitant, I = interacting.
SUSPECT_ROLES = {"PS", "SS"}

# ---------------------------------------------------------------------------
# Signal-detection thresholds (classic Evans et al. 2001 criteria for PRR)
# ---------------------------------------------------------------------------
MIN_CASES = 3        # minimum co-reported cases (a) to consider a pair
PRR_THRESHOLD = 2.0  # PRR >= 2
CHI2_THRESHOLD = 4.0 # chi-squared >= 4
